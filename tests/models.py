from google.appengine.ext import blobstore, db, ndb
from webapp2 import cached_property

from restler.decorators import ae_db_serializer, ae_ndb_serializer


@ae_db_serializer
@ae_db_serializer
class Model2(db.Model):
    model2_prop = db.StringProperty()

    @property
    def my_method(self):
        return "I say blah!"

    @cached_property
    def my_cached_property(self):
        return "my cached property"


@ae_db_serializer
class Model1(db.Model):
    string = db.StringProperty()
    bytestring = db.ByteStringProperty()
    boolean = db.BooleanProperty()
    integer = db.IntegerProperty()
    float_ = db.FloatProperty()
    datetime = db.DateTimeProperty()
    date = db.DateProperty()
    time = db.TimeProperty()
    list_ = db.ListProperty(long)
    stringlist = db.StringListProperty()
    reference = db.ReferenceProperty(reference_class=Model2, collection_name="references")
    selfreference = db.SelfReferenceProperty(collection_name="models")
    blobreference = blobstore.BlobReferenceProperty()
    user = db.UserProperty()
    blob = db.BlobProperty()
    text = db.TextProperty()
    category = db.CategoryProperty()
    link = db.LinkProperty()
    email = db.EmailProperty()
    geopt = db.GeoPtProperty()
    im = db.IMProperty()
    phonenumber = db.PhoneNumberProperty()
    postaladdress = db.PostalAddressProperty()
    rating = db.RatingProperty()


@ae_ndb_serializer
class NdbModel2(ndb.Model):
    model2_prop = ndb.StringProperty()

    @property
    def my_method(self):
        return "I say blah!"

    @cached_property
    def my_cached_property(self):
        return "my cached property"


@ae_ndb_serializer
class NdbModel1(ndb.Model):
    string = ndb.StringProperty()
    boolean = ndb.BooleanProperty()
    integer = ndb.IntegerProperty()
    float_ = ndb.FloatProperty()
    datetime = ndb.DateTimeProperty(auto_now=True)
    date = ndb.DateProperty()
    time = ndb.TimeProperty()
    user = ndb.UserProperty()
    blob = ndb.BlobProperty()
    text = ndb.TextProperty()
    geopt = ndb.GeoPtProperty()
    stringlist = ndb.StringProperty(repeated=True)
    integerlist = ndb.IntegerProperty(repeated=True)
    json_ = ndb.JsonProperty()
    # blob_key = ndb.BlobKeyProperty()
    # structured = ndb.StructuredProperty()
    # local_structured = ndb.LocalStructuredProperty()


@ae_ndb_serializer
class NdbModel3(ndb.Model):
    generic = ndb.GenericProperty()
    name = ndb.StringProperty()
    name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
    pickle_ = ndb.PickleProperty()
