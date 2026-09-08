commands_require_target = [
    "go",
    "take",
    "drop",
    "use",
    "attack"
]
commands_optional_target = [
    "look"
]
commands_forbid_target = [
    "inventory"
]

def parse_command(user_input,commands_require_target,commands_optional_target,commands_forbid_target):
    supported_commands = commands_require_target.union(
        commands_optional_target,
        commands_forbid_target
    )
    
    command_split = user_input.split()
    if not command_split:
        print("User supplied: ", [command_split])
        return None

    if command_split[0] not in supported_commands:
        print("Unsupported command. Please enter valide command...")
        return None
    
    target_split = command_split[1:]
    if command_split[0] in commands_require_target:
        if not target_split:
            print([command_split[0]], "requires a target...")
            return None
        else:
            target = " ".join(target_split).lower()
    
    if command_split[0] in commands_optional_target:
        if not target_split:
            target = None
        else:
            target = " ".join(target_split).lower()
    
    if command_split[0] in commands_forbid_target:
        if target_split:
            print([command_split[0]], "does not accept a target...")
            return None
        else:
            target = None

    parsed_command = {
        "command": command_split[0].lower(),
        "target": target
    }
    
    return parsed_command