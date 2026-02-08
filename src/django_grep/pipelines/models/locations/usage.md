# Locations Module Usage

This module provides models for managing geographical locations, addresses, and corporate branches.

## Classes

### Country
- **File**: `city.py`
- **Description**: Represents a country.
- **Usage**:
  ```python
  from django_grep.pipelines.models.locations.city import Country
  egypt = Country.objects.create(name="Egypt")
  cities = egypt.get_cities()
  ```

### City
- **File**: `city.py`
- **Description**: Represents a city within a country.
- **Usage**:
  ```python
  from django_grep.pipelines.models.locations.city import City
  cairo = City.objects.create(name="Cairo", country=egypt)
  ```

### Address
- **File**: `address.py`
- **Description**: Represents a detailed physical address.
- **Usage**:
  ```python
  from django_grep.pipelines.models.locations.address import Address
  addr = Address.objects.create(
      city=cairo,
      street="Main St",
      building="10",
      apartment="4",
      postal_code="12345"
  )
  ```

### Branch
- **File**: `branch.py`
- **Description**: Represents a branch location of a corporate entity.
- **Usage**:
  ```python
  from django_grep.pipelines.models.locations.branch import Branch
  branch = Branch.objects.create(
      name="Heliopolis Branch",
      corporate=corporate_instance,
      code="B001",
      location="Cairo",
      address="Full address here",
      opening_time="09:00:00",
      closing_time="17:00:00"
  )
  ```

## Planned/Future Fields & Models

The following code was previously commented out in the source files and is preserved here for future reference:

### Country Extensions
```python
# From city.py
# region = models.ForeignKey(( "location.Region"), null=True, on_delete=models.DO_NOTHING)
# city = models.ForeignKey(( "commons.City"), null=True, on_delete=models.DO_NOTHING)
```

### Address Extensions
```python
# From address.py
# country = models.ForeignKey(('location.Country'), on_delete=models.CASCADE)
```

### Region Model (Previously in city.py)
```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    region = models.CharField(max_length=100, null=True, verbose_name=_("Region"))

    # location = models.CharField(max_length=100, null=True, verbose_name=_('Location'))
    # country = models.ForeignKey(('Client.Country'), on_delete=models.CASCADE)
    # Corporate = models.ForeignKey(('Organisations.Corporate'), on_delete=models.CASCADE)
    # stock = models.ForeignKey(('Stocks.Stock'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ["name"]
        db_table = "Regions"

    def __str__(self):
        return f"{self.name}"
```

### Other Imports
```python
# # from core.app.models import *
```
