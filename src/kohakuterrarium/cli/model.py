"""CLI model management commands — list, default, show LLM profiles."""

import argparse

from kohakuterrarium.llm.profiles import (
    get_default_model,
    get_profile,
    list_all,
    set_default_model,
)


def model_cli(args: argparse.Namespace) -> int:
    """Manage LLM profiles."""
    sub = getattr(args, "model_command", None)

    if sub == "list" or sub is None:
        default = get_default_model()
        entries = list_all()
        if default:
            print(f"Default model: {default}")
        else:
            print("No default model set. Use: kt model default <name>")
        print()
        print(
            f"{'Name':<25} {'Model':<40} {'Login':<12} {'Context':<10} {'Src':<6} {'Status'}"
        )
        print("-" * 105)
        for e in entries:
            marker = " *" if e.get("is_default") else ""
            ctx = e.get("max_context", 0)
            ctx_str = f"{ctx // 1000}k" if ctx else ""
            login = e.get("login_provider", "")
            available = e.get("available", False)
            status = "ok" if available else f"(kt login {login})"
            print(
                f"{e['name']:<25} {e['model']:<40} {login:<12} {ctx_str:<10} {e['source']:<6} {status}{marker}"
            )
        return 0

    elif sub == "default":
        name = args.name
        # Verify the profile exists
        profile = get_profile(name)
        if not profile:
            print(f"Profile/preset not found: {name}")
            print("Use 'kt model list' to see available options.")
            return 1
        set_default_model(name)
        print(f"Default model set to: {name} ({profile.model})")
        return 0

    elif sub == "show":
        name = args.name
        profile = get_profile(name)
        if not profile:
            print(f"Profile/preset not found: {name}")
            return 1
        print(f"Name:       {profile.name}")
        print(f"Provider:   {profile.provider}")
        print(f"Model:      {profile.model}")
        print(f"Context:    {profile.max_context:,} tokens")
        print(f"Max output: {profile.max_output:,} tokens")
        if profile.base_url:
            print(f"Base URL:   {profile.base_url}")
        if profile.api_key_env:
            print(f"API key:    ${profile.api_key_env}")
        if profile.temperature is not None:
            print(f"Temperature: {profile.temperature}")
        if profile.reasoning_effort:
            print(f"Reasoning:  {profile.reasoning_effort}")
        if profile.extra_body:
            print(f"Extra body: {profile.extra_body}")
        return 0

    print("Usage: kt model [list|default <name>|show <name>]")
    return 0
