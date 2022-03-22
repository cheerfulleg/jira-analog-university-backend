import re

from passlib.handlers.bcrypt import bcrypt
from tortoise import Model, fields, Tortoise
from tortoise.validators import RegexValidator

REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class User(Model):
    """
    User model
    """

    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(120, validators=[RegexValidator(REGEX, re.I)], unique=True)
    password = fields.CharField(128)
    first_name = fields.CharField(50)
    last_name = fields.CharField(50)
    is_active = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now=True)

    team_member: fields.ReverseRelation["TeamMember"]

    class PydanticMeta:
        exclude = ("password", "created_at", "is_active")

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    @staticmethod
    def create_password_hash(password):
        return bcrypt.hash(password)

    def __str__(self) -> str:
        return self.email


class TeamMember(Model):
    user = fields.ForeignKeyField("models.User", related_name="team_member")
    project = fields.ForeignKeyField("models.Project", related_name="team_members")
    role = fields.CharField(100, null=True, default=None)

    class PydanticMeta:
        unique_together = (("project", "user"),)


class Project(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(250)
    description = fields.TextField(null=True, default=None)

    team_members: fields.ReverseRelation["TeamMember"]
    columns: fields.ReverseRelation["Column"]

    def __str__(self):
        return self.name


class Column(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(50)
    project = fields.ForeignKeyField("models.Project", related_name="columns")


Tortoise.init_models(["backend.core.app.models"], "models")
