from dataclasses import dataclass, field
from agent import Agent


@dataclass
class Object:
    name: str
    description: str
    is_usable: bool
    # e.g., {"status": "available"}, {"status": "in_use", "by_agent": "Alex"}
    state: dict = field(default_factory=dict)

    def is_available(self) -> bool:
        return self.state.get("status", "available") == "available"


@dataclass
class Location:
    name: str
    description: str
    objects: dict[str, Object] = field(default_factory=dict)
    connections: list[str] = field(default_factory=list)

    def add_object(self, obj: Object):
        self.objects[obj.name] = obj

    def get_object(self, object_name: str) -> Object | None:
        return self.objects.get(object_name)

    def use_object(self, object_name: str, agent_id: str) -> bool:
        obj = self.get_object(object_name)
        if obj and obj.is_usable and obj.is_available():
            obj.state["status"] = "in_use"
            obj.state["by_agent"] = agent_id
            return True
        return False

    def release_object(self, object_name: str):
        obj = self.get_object(object_name)
        if obj and not obj.is_available():
            obj.state["status"] = "available"
            obj.state.pop("by_agent", None)


@dataclass
class WorldProfile:
    name: str
    description: str
    locations: dict[str, Location] = field(default_factory=dict)

    def add_location(self, loc: Location):
        self.locations[loc.name] = loc

    def get_location(self, location_name: str) -> Location | None:
        return self.locations.get(location_name)


@dataclass
class WorldState:
    agen
