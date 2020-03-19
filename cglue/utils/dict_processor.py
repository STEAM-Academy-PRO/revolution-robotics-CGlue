from typing import Dict, Any, Set


class DictProcessor:
    def __init__(self, required_keys: Set[str], optional_keys: Dict[str, Any]):
        self._required = required_keys
        self._optional = optional_keys
        self._optional_keys = set(self._optional.keys())

    def process(self, target: Dict[str, Any]):
        """This function makes sure src contains required and optional keys and nothing else"""

        present_keys = set(target.keys())

        missing_required = self._required - present_keys
        not_required = present_keys - self._required
        unexpected_keys = not_required - self._optional_keys

        if unexpected_keys:
            raise Exception(f'Unexpected keys: {", ".join(unexpected_keys)}')

        if missing_required:
            raise Exception(f'Missing keys: {", ".join(missing_required)}')

        return {**self._optional, **target}
