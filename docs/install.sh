#!/usr/bin/env bash
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

REPO_URL="https://github.com/apiad/opencode-core.git"

banner() {
    echo ""
    echo -e "${BOLD}OpenCode Opinionated Framework Installer${NC}"
    echo ""
}

error() {
    echo -e "${RED}Error: $*${NC}" >&2
    exit 1
}

info() {
    echo -e "${CYAN}→${NC} $*"
}

success() {
    echo -e "${GREEN}✓${NC} $*"
}

warn() {
    echo -e "${YELLOW}⚠${NC} $*"
}

check_git() {
    if ! command -v git &>/dev/null; then
        error "Git is not installed. Please install git first: https://git-scm.com"
    fi
    info "Git found: $(git --version | head -1)"
}

check_uv() {
    if ! command -v uv &>/dev/null; then
        error "uv is not installed. Please install it: https://github.com/astral-sh/uv"
    fi
    info "uv found: $(uv --version | head -1)"
}

check_opencode() {
    if [[ ! -x "$HOME/.opencode/bin/opencode" ]]; then
        error "OpenCode CLI not found. Please install it:
    curl -fsSL https://opencode.ai/install | bash"
    fi
    info "OpenCode CLI found"
}

check_git_clean() {
    if [[ -n "$(git status --porcelain)" ]]; then
        error "Git working tree not clean. Please commit or stash your changes first."
    fi
    info "Git working tree is clean"
}

check_not_installed() {
    if [[ -d ".opencode" ]]; then
        error ".opencode/ already exists. Remove it first if you want to reinstall."
    fi
}

parse_args() {
    mode="copy"
    for arg in "$@"; do
        case "$arg" in
            --link) mode="link" ;;
            --help)
                echo "Usage: $0 [--link]"
                echo ""
                echo "  --link    Add framework as git submodule (get upstream updates)"
                echo "            Default: copy mode (self-contained)"
                exit 0
                ;;
            *)
                error "Unknown option: $arg. Use --help for usage."
                ;;
        esac
    done
}

install_copy() {
    info "Installing OpenCode Framework (copy mode)..."

    temp_dir=$(mktemp -d)
    git clone --depth 1 "$REPO_URL" "$temp_dir/opencode-core"
    mv "$temp_dir/opencode-core" .opencode
    rm -rf "$temp_dir"

    if [[ -d ".opencode/.git" ]]; then
        rm -rf ".opencode/.git"
    fi

    success "Framework installed to .opencode/"
}

install_link() {
    info "Installing OpenCode Framework (link mode)..."
    git submodule add --force "$REPO_URL" .opencode
    success "Framework linked as git submodule at .opencode/"
}

create_directories() {
    info "Creating .knowledge/ directories..."
    mkdir -p .knowledge/{notes,plans,log,drafts}
    success "Directories created"
}

main() {
    banner
    parse_args "$@"

    check_git
    check_uv
    check_opencode
    check_not_installed
    check_git_clean

    case "$mode" in
        copy) install_copy ;;
        link) install_link ;;
    esac

    create_directories

    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Installation complete!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "Next steps:"
    echo -e "  ${CYAN}opencode /help${NC}    - Learn how to use this framework"
    echo -e "  ${CYAN}opencode /onboard${NC} - Get started with your project"
    echo ""
    if [[ "$mode" == "link" ]]; then
        echo -e "To update framework later:"
        echo -e "  ${CYAN}cd .opencode && git pull${NC}"
        echo ""
    fi
}

main "$@"
