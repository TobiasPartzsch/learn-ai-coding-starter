from dataclasses import dataclass
from enum import Enum, auto

from sloperator.errors import SlopRuntimeError
from sloperator.evaluator.values import Value


class BindingKind(Enum):
    MUTABLE = auto()
    CONSTANT = auto()
    FUNCTION = auto()


@dataclass
class Binding:
    value: Value
    kind: BindingKind


class Environment:
    def __init__(self, parent: "Environment | None" = None) -> None:
        self.bindings: dict[str, Binding] = {}
        self.parent = parent

    def declare(self, name: str, value: Value, kind: BindingKind, line: int) -> None:
        if name in self.bindings:
            raise SlopRuntimeError(line, f"'{name}' is already declared in this scope")
        self.bindings[name] = Binding(value, kind)

    def get(self, name: str, line: int) -> Value:
        return self.lookup(name, line).value

    def assign(self, name: str, value: Value, line: int) -> None:
        self.assignment_target(name, line).value = value

    def get_for_assignment(self, name: str, line: int) -> Value:
        return self.assignment_target(name, line).value

    def assignment_target(self, name: str, line: int) -> Binding:
        binding = self.lookup(name, line)
        match binding.kind:
            case BindingKind.MUTABLE:
                return binding
            case BindingKind.CONSTANT:
                raise SlopRuntimeError(line, f"cannot assign to loadbearing '{name}'")
            case BindingKind.FUNCTION:
                raise SlopRuntimeError(line, f"cannot assign to immutable binding '{name}'")
        raise AssertionError("unreachable")

    def lookup(self, name: str, line: int) -> Binding:
        env: Environment | None = self
        while env is not None:
            if name in env.bindings:
                return env.bindings[name]
            env = env.parent
        raise SlopRuntimeError(line, f"undefined variable '{name}'")
