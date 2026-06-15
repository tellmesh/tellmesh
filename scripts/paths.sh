#!/usr/bin/env bash
# Shared TellMesh path variables for examples and shell scripts.
# Source from monorepo root: source "$ROOT/scripts/paths.sh"
TELLMESH_ORG="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd)"
HV_SCRIPTS="${TELLMESH_ORG}/resource-agent-hypervisor/scripts"
WWW_SCRIPTS="${TELLMESH_ORG}/www/scripts"
