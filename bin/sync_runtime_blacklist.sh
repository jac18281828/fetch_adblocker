#!/usr/bin/env bash

set -euo pipefail

SOURCE_CONF="${SOURCE_CONF:-/etc/dnsmasq.d/blacklist.conf}"
RUNTIME_CONF_DIR="${RUNTIME_CONF_DIR:-/run/dnsmasq.dhcp.conf.d}"
RUNTIME_CONF="${RUNTIME_CONF:-${RUNTIME_CONF_DIR}/blacklist.conf}"
DNSMASQ_PIDFILE="${DNSMASQ_PIDFILE:-/run/dnsmasq-main.pid}"
WAIT_SECONDS="${WAIT_SECONDS:-30}"

if [[ ! -f "${SOURCE_CONF}" ]]; then
    echo "Source ${SOURCE_CONF} not found; skipping"
    exit 0
fi

# UniFi creates the runtime dnsmasq directory during startup.
for ((i = 0; i < WAIT_SECONDS; i++)); do
    if [[ -d "${RUNTIME_CONF_DIR}" ]]; then
        break
    fi
    sleep 1
done

mkdir -p "${RUNTIME_CONF_DIR}"

if [[ -f "${RUNTIME_CONF}" ]] && cmp -s "${SOURCE_CONF}" "${RUNTIME_CONF}"; then
    echo "Runtime blacklist already current"
    exit 0
fi

install -m 0644 "${SOURCE_CONF}" "${RUNTIME_CONF}"
echo "Installed ${RUNTIME_CONF}"

if [[ -r "${DNSMASQ_PIDFILE}" ]]; then
    dnsmasq_pid="$(cat "${DNSMASQ_PIDFILE}")"
    if kill -0 "${dnsmasq_pid}" 2>/dev/null; then
        kill -HUP "${dnsmasq_pid}"
        echo "Reloaded dnsmasq (${dnsmasq_pid})"
    else
        echo "dnsmasq pid ${dnsmasq_pid} is not running; copied config only" >&2
    fi
else
    echo "dnsmasq pidfile ${DNSMASQ_PIDFILE} not found; copied config only" >&2
fi
