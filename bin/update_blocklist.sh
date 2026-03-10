#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${SCRIPT_DIR}/fetch_masq.py" ]]; then
    REPO_ROOT="${SCRIPT_DIR}"
elif [[ -f "${SCRIPT_DIR}/../fetch_masq.py" ]]; then
    REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
else
    echo "Could not locate fetch_masq.py relative to ${SCRIPT_DIR}" >&2
    exit 1
fi

STATIC_CONF="${STATIC_CONF:-/etc/dnsmasq.d/blacklist.conf}"
RUNTIME_CONF_DIR="${RUNTIME_CONF_DIR:-/run/dnsmasq.dhcp.conf.d}"
RUNTIME_CONF="${RUNTIME_CONF:-${RUNTIME_CONF_DIR}/blacklist.conf}"
DNSMASQ_PIDFILE="${DNSMASQ_PIDFILE:-/run/dnsmasq-main.pid}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SOURCE_URL="${SOURCE_URL:-}"
TMP_CONF="$(mktemp "${TMPDIR:-/tmp}/blacklist.conf.XXXXXX")"
trap 'rm -f "${TMP_CONF}"' EXIT

cd "${REPO_ROOT}"

echo 'Fetching Blacklist'
if [[ -n "${SOURCE_URL}" ]]; then
    "${PYTHON_BIN}" fetch_masq.py "${SOURCE_URL}" > "${TMP_CONF}"
else
    "${PYTHON_BIN}" fetch_masq.py > "${TMP_CONF}"
fi

mkdir -p "$(dirname "${STATIC_CONF}")" "${RUNTIME_CONF_DIR}"

static_changed=0
runtime_changed=0

if [[ ! -f "${STATIC_CONF}" ]] || ! cmp -s "${TMP_CONF}" "${STATIC_CONF}"; then
    install -m 0644 "${TMP_CONF}" "${STATIC_CONF}"
    static_changed=1
fi

if [[ ! -f "${RUNTIME_CONF}" ]] || ! cmp -s "${STATIC_CONF}" "${RUNTIME_CONF}"; then
    install -m 0644 "${STATIC_CONF}" "${RUNTIME_CONF}"
    runtime_changed=1
fi

wc -l "${STATIC_CONF}"

if [[ "${static_changed}" -eq 0 && "${runtime_changed}" -eq 0 ]]; then
    echo "Blacklist unchanged"
    exit 0
fi

if [[ -r "${DNSMASQ_PIDFILE}" ]]; then
    dnsmasq_pid="$(cat "${DNSMASQ_PIDFILE}")"
    if kill -0 "${dnsmasq_pid}" 2>/dev/null; then
        kill -HUP "${dnsmasq_pid}"
        echo "Reloaded dnsmasq (${dnsmasq_pid})"
    else
        echo "dnsmasq pid ${dnsmasq_pid} is not running; skipped reload" >&2
    fi
else
    echo "dnsmasq pidfile ${DNSMASQ_PIDFILE} not found; skipped reload" >&2
fi
