from env_setup import setup_django; setup_django()

from django.db import models, connection

from restler import decorators


@decorators.django_serializer
class Model1(models.Model):
    big_integer = models.BigIntegerField(null=True, default=1)
    boolean = models.BooleanField(default=False)
    char = models.CharField(max_length=10, null=True, default="CharField")
    comma_separated_int = models.CommaSeparatedIntegerField(max_length=20, default=[1, 2, 3])
    _date = models.DateField(null=True, auto_now=True)
    _datetime = models.DateTimeField(null=True, auto_now=True)
    decimal = models.DecimalField(max_digits=20, decimal_places=2, null=True, default="10.20")
    email = models.EmailField(null=True, default="test@test.com")
    _float = models.FloatField(null=True, default=10.2)
    integer = models.IntegerField(null=True, default=2)
    ip_address = models.IPAddressField(null=True, default="127.0.0.1")
    null_boolean = models.NullBooleanField(null=True)
    positive_int = models.PositiveIntegerField(null=True, default=2)
    positive_small_int = models.PositiveSmallIntegerField(null=True, default=2)
    slug = models.SlugField(null=True, default="Some combination of 1 23")
    small_int = models.SmallIntegerField(null=True, default=2)
    text = models.TextField(null=True, default="Some Text")
    _time = models.TimeField(null=True, auto_now=True)
    url = models.URLField(null=True, default="http://www.yahoo.com")

    # unsupported types
    _file = models.FileField(upload_to=".", null=True)
    file_path = models.FilePathField(null=True)
    image = models.ImageField(upload_to=".")

    # Relationship fields
    rel1 = models.ForeignKey("Model1", related_name="set1", null=True)
    rel2 = models.ManyToManyField("Model1", related_name="set2", null=True)
    rel3 = models.OneToOneField("Model1", null=True)

    class Meta:
        app_label = 'test'

    def __unicode__(self):
        return "Model1 -> %s, %s, %s" % (self.id, self.big_integer, self.char)


@decorators.django_serializer
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    class Meta:
        app_label = 'test'


@decorators.django_serializer
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    class Meta:
        app_label = 'test'


def install_model(model):
    from django.core.management import color

    # Standard syncdb expects models to be in reliable locations,
    # so dynamic models need to bypass django.core.management.syncdb.
    # On the plus side, this allows individual models to be installed
    # without installing the entire project structure.
    # On the other hand, this means that things like relationships and
    # indexes will have to be handled manually.
    # This installs only the basic table definition.

    # disable terminal colors in the sql statements
    style = color.no_style()

    cursor = connection.cursor()
    statements, pending = connection.creation.sql_create_model(model, style)
    for stmt in statements:
        cursor.execute(stmt)
