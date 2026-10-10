from __future__ import annotations

import json
import math
import re
from collections import Counter
from typing import Any, Dict, Iterable, Optional, Sequence, Tuple
from urllib.parse import parse_qsl, urlsplit


# Top 25 intra-request HTTP features proposed for the thesis experiments.
TOP25_HTTP_FEATURES = [
    "body_encoded_ratio",
    "uri_encoded_ratio",
    "path_depth",
    "uri_non_alnum_ratio",
    "max_param_value_len",
    "body_len",
    "uri_len",
    "query_len",
    "n_query_params",
    "req_content_length",
    "uri_entropy",
    "body_entropy",
    "invalid_percent_encoding_count",
    "double_encoding_count",
    "path_traversal_token_count",
    "sql_token_count",
    "xss_token_count",
    "cmd_injection_token_count",
    "file_inclusion_token_count",
    "quote_comment_operator_count",
    "repeated_param_name_count",
    "empty_param_value_ratio",
    "avg_param_value_len",
    "content_length_body_mismatch",
    "content_type_body_mismatch",
]

_HEX = r"[0-9a-fA-F]"
_PCT_ENC_RE = re.compile(rf"%{_HEX}{{2}}")
_INVALID_PERCENT_RE = re.compile(rf"%(?!{_HEX}{{2}})")
_DOUBLE_ENC_RE = re.compile(rf"%25{_HEX}{{2}}", re.IGNORECASE)

# Regex groups intentionally use broad attack-family indicators. They are still
# intra-request features: they only inspect the current URI, body and headers.
PATH_TRAVERSAL_PATTERNS: Sequence[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\.\./",
        r"\.\.\\",
        r"\.\.%2f",
        r"\.\.%5c",
        r"%2e%2e(?:%2f|/|%5c|\\)?",
        r"%252e%252e(?:%252f|%255c)?",
        r"/etc/passwd",
        r"/proc/self",
        r"boot\.ini",
        r"win\.ini",
    ]
]

SQL_PATTERNS: Sequence[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bunion\b",
        r"\bselect\b",
        r"\binsert\b",
        r"\bupdate\b",
        r"\bdelete\b",
        r"\bdrop\b",
        r"\bfrom\b",
        r"\bwhere\b",
        r"\binformation_schema\b",
        r"\bor\s+1\s*=\s*1\b",
        r"\band\s+1\s*=\s*1\b",
        r"sleep\s*\(",
        r"benchmark\s*\(",
        r"load_file\s*\(",
        r"into\s+outfile",
        r"waitfor\s+delay",
        r"xp_cmdshell",
        r"--",
        r"/\*",
        r"\*/",
    ]
]

XSS_PATTERNS: Sequence[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"<\s*script\b",
        r"</\s*script\s*>",
        r"<\s*img\b",
        r"<\s*svg\b",
        r"<\s*iframe\b",
        r"onerror\s*=",
        r"onload\s*=",
        r"onclick\s*=",
        r"javascript\s*:",
        r"document\.cookie",
        r"alert\s*\(",
        r"eval\s*\(",
    ]
]

CMD_INJECTION_PATTERNS: Sequence[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"&&",
        r"\|\|",
        r";",
        r"`",
        r"\$\(",
        r"\bcat\s+",
        r"\bwget\b",
        r"\bcurl\b",
        r"/bin/sh",
        r"/bin/bash",
        r"\bcmd\.exe\b",
        r"\bpowershell\b",
        r"\bwhoami\b",
        r"\bchmod\b",
        r"\brm\s+-rf\b",
        r"\bnc\s+",
    ]
]

FILE_INCLUSION_PATTERNS: Sequence[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"file://",
        r"php://",
        r"zip://",
        r"data://",
        r"expect://",
        r"http://",
        r"https://",
        r"ftp://",
        r"\.\./",
        r"%00",
        r"/etc/passwd",
        r"boot\.ini",
        r"win\.ini",
    ]
]

QUOTE_COMMENT_OPERATOR_PATTERNS: Sequence[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"'",
        r'"',
        r"--",
        r"#",
        r"/\*",
        r"\*/",
        r"=",
        r"<",
        r">",
    ]
]


def _ratio(n: int | float, d: int | float) -> float:
    return float(n) / float(d) if d else 0.0


def _entropy(text: str) -> float:
    if not text:
        return 0.0
    counts = Counter(text)
    total = float(len(text))
    return float(-sum((c / total) * math.log2(c / total) for c in counts.values()))


def _decode_body(body: Optional[bytes]) -> str:
    if body is None:
        return ""
    if isinstance(body, bytes):
        return body.decode("utf-8", errors="ignore")
    return str(body)


def _headers_lower(headers: Optional[Dict[str, str]]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for k, v in (headers or {}).items():
        out[str(k).strip().lower()] = str(v).strip()
    return out


def _parse_content_length(headers_lc: Dict[str, str]) -> Tuple[int, bool]:
    raw = headers_lc.get("content-length")
    if raw is None or raw == "":
        return 0, False
    try:
        val = int(str(raw).strip())
        return max(val, 0), True
    except Exception:
        return 0, True


def _count_patterns(text: str, patterns: Sequence[re.Pattern[str]]) -> int:
    if not text:
        return 0
    return int(sum(len(p.findall(text)) for p in patterns))


def _query_params(query: str) -> list[tuple[str, str]]:
    if not query:
        return []
    return [(str(k), str(v)) for k, v in parse_qsl(query, keep_blank_values=True, strict_parsing=False)]


def _looks_form_like(body_text: str, content_type: str) -> bool:
    if not body_text:
        return False
    ct = (content_type or "").lower()
    stripped = body_text.strip()
    if "application/x-www-form-urlencoded" in ct:
        return True
    if "multipart/form-data" in ct:
        return False
    if stripped.startswith("{") or stripped.startswith("[") or stripped.startswith("<"):
        return False
    return "=" in stripped or "&" in stripped


def _body_params(body_text: str, content_type: str) -> list[tuple[str, str]]:
    if not _looks_form_like(body_text, content_type):
        return []
    return [(str(k), str(v)) for k, v in parse_qsl(body_text, keep_blank_values=True, strict_parsing=False)]


def _repeated_name_count(params: Iterable[tuple[str, str]]) -> int:
    names = [k for k, _ in params]
    if not names:
        return 0
    counts = Counter(names)
    return int(sum(c - 1 for c in counts.values() if c > 1))


def _content_type_body_mismatch(content_type: str, body_text: str) -> int:
    """Return 1 when Content-Type declares a body format that the body does not match."""
    ct = (content_type or "").lower()
    stripped = (body_text or "").strip()
    if not ct or not stripped:
        return 0

    if "application/json" in ct or ct.endswith("+json"):
        try:
            json.loads(stripped)
            return 0
        except Exception:
            return 1

    if "application/x-www-form-urlencoded" in ct:
        # A non-empty urlencoded body should contain at least one key=value pair.
        if "=" not in stripped:
            return 1
        return 0 if len(parse_qsl(stripped, keep_blank_values=True, strict_parsing=False)) > 0 else 1

    if "xml" in ct:
        return 0 if stripped.startswith("<") and ">" in stripped else 1

    if "multipart/form-data" in ct:
        # Very conservative: if a boundary is declared, it should appear in the body.
        m = re.search(r"boundary=([^;]+)", ct, flags=re.IGNORECASE)
        if m:
            boundary = m.group(1).strip().strip('"')
            return 0 if boundary and boundary in stripped else 1
        return 1

    return 0


def extract_http_features(
    *,
    method: str,
    uri: str,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[bytes] = None,
) -> Dict[str, Any]:
    """Compute the proposed top-25 intra-request HTTP features.

    The extractor intentionally avoids application baselines, session context,
    historical traffic windows, IP reputation, user identity or any external
    source. It only uses method/URI/headers/body from the current request.
    """
    del method  # Method is intentionally not part of the proposed top-25 set.

    uri_text = uri or ""
    body_text = _decode_body(body)
    combined_text = f"{uri_text}\n{body_text}"

    headers_lc = _headers_lower(headers)
    content_type = headers_lc.get("content-type", "")
    req_content_length, has_content_length = _parse_content_length(headers_lc)

    body_len = len(body) if isinstance(body, bytes) else len(body_text.encode("utf-8", errors="ignore"))
    if not has_content_length and body_len > 0:
        # Useful for datasets where Content-Length is omitted but the parsed body is available.
        req_content_length = body_len

    parts = urlsplit(uri_text)
    path = parts.path or ""
    query = parts.query or ""

    uri_len = len(uri_text)
    query_len = len(query)
    path_depth = len([p for p in path.split("/") if p])

    q_params = _query_params(query)
    b_params = _body_params(body_text, content_type)
    all_params = q_params + b_params
    values = [v for _, v in all_params]

    n_query_params = len(q_params)
    max_param_value_len = max((len(v) for v in values), default=0)
    avg_param_value_len = float(sum(len(v) for v in values) / len(values)) if values else 0.0
    empty_param_value_ratio = _ratio(sum(1 for v in values if v == ""), len(values))
    repeated_param_name_count = _repeated_name_count(all_params)

    uri_non_alnum_ratio = _ratio(sum(1 for ch in uri_text if not ch.isalnum()), uri_len)
    uri_encoded_ratio = _ratio(len(_PCT_ENC_RE.findall(uri_text)) * 3, uri_len)
    body_encoded_ratio = _ratio(len(_PCT_ENC_RE.findall(body_text)) * 3, len(body_text))

    invalid_percent_encoding_count = len(_INVALID_PERCENT_RE.findall(combined_text))
    double_encoding_count = len(_DOUBLE_ENC_RE.findall(combined_text))

    content_length_body_mismatch = int(has_content_length and req_content_length != body_len)
    content_type_body_mismatch = _content_type_body_mismatch(content_type, body_text)

    feats: Dict[str, Any] = {
        "body_encoded_ratio": body_encoded_ratio,
        "uri_encoded_ratio": uri_encoded_ratio,
        "path_depth": path_depth,
        "uri_non_alnum_ratio": uri_non_alnum_ratio,
        "max_param_value_len": max_param_value_len,
        "body_len": body_len,
        "uri_len": uri_len,
        "query_len": query_len,
        "n_query_params": n_query_params,
        "req_content_length": req_content_length,
        "uri_entropy": _entropy(uri_text),
        "body_entropy": _entropy(body_text),
        "invalid_percent_encoding_count": invalid_percent_encoding_count,
        "double_encoding_count": double_encoding_count,
        "path_traversal_token_count": _count_patterns(combined_text, PATH_TRAVERSAL_PATTERNS),
        "sql_token_count": _count_patterns(combined_text, SQL_PATTERNS),
        "xss_token_count": _count_patterns(combined_text, XSS_PATTERNS),
        "cmd_injection_token_count": _count_patterns(combined_text, CMD_INJECTION_PATTERNS),
        "file_inclusion_token_count": _count_patterns(combined_text, FILE_INCLUSION_PATTERNS),
        "quote_comment_operator_count": _count_patterns(combined_text, QUOTE_COMMENT_OPERATOR_PATTERNS),
        "repeated_param_name_count": repeated_param_name_count,
        "empty_param_value_ratio": empty_param_value_ratio,
        "avg_param_value_len": avg_param_value_len,
        "content_length_body_mismatch": content_length_body_mismatch,
        "content_type_body_mismatch": content_type_body_mismatch,
    }

    return feats
