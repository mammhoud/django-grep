# Django GREP Pipelines Models Usage

This document provides usage examples for various models in the `django-grep` pipelines.

## Tags

### Tag
- **File**: `tags.py`
- **Description**: Enhanced tagging system for general content.
- **Example**:
  ```python
  from django_grep.pipelines.models.tags import Tag
  tag = Tag.objects.create(name="Innovation", color="#3B82F6")
  ```

### PersonTag
- **File**: `tags.py`
- **Description**: Specialized tags for persons with expiration and verification features.

---

## Users & Roles

### Role
- **File**: `users/role.py`
- **Description**: Defines user roles and hierarchical levels.
- **Example**:
  ```python
  from django_grep.pipelines.models.users.role import Role
  admin_role = Role.objects.create(name="Admin", level=10, is_default=False)
  ```

### Team
- **File**: `users/team.py`
- **Description**: Comprehensive team management with memberships and invitations.
- **Example**:
  ```python
  from django_grep.pipelines.models.users.team import Team
  team = Team.objects.create(name="Engineering", department=dept)
  team.add_member(person, role="leader")
  ```

---

## Contacts

### ProfessionalBase
- **File**: `contacts/contact.py`
- **Description**: Abstract base for professional relationships and organizational links.

---

## Settings

### SiteSettings
- **File**: `settings/settings.py`
- **Description**: Global website branding and SEO settings per language.

### SocialSettings
- **File**: `settings/settings.py`
- **Description**: Site-wide contact details and social links.

### NewsletterSubscription
- **File**: `settings/subscription.py`
- **Description**: Tracks user newsletter subscriptions.

---

## Archived Code (Reserved for Future Use)

### Tags Metadata & Relationships
```python
# From tags.py
# Tag importance or visibility filters
index.FilterField("live")

# Related Tags Relationship
# related_tags = models.ManyToManyField(
#     'self',
#     blank=True,
#     symmetrical=False,
#     through='TagRelationship',
#     through_fields=('source_tag', 'target_tag'),
#     related_name='related_to',
#     verbose_name=_("Related Tags"),
#     help_text=_("Manually curated related tags")
# )
```

### User Role Groups Helper
```python
# From role.py
# @classmethod
# def user_role_groups(cls, user):
#     if not user:
#         raise ValidationError("A valid user instance is required.")
#     role = getattr(user, "role", None)
#     user_groups = user.groups.all()
#     return {
#         "role": {"id": role.pk if role else None, "name": role.name},
#         "group": {"id": role.group.pk if role and role.group else None},
#         "user_groups": [{"id": g.pk, "name": g.name} for g in user_groups],
#     }
```

### Team Leadership Logic
```python
# From team.py
# @property
# def is_leader(self):
#     return self.role in [self.MemberRole.LEADER, self.MemberRole.DEPUTY_LEADER]

# @property
# def leadership(self):
#     return self.memberships.filter(
#         role__in=[TeamMembership.MemberRole.LEADER, TeamMembership.MemberRole.DEPUTY_LEADER],
#         status=TeamMembership.MembershipStatus.ACTIVE
#     )
```
