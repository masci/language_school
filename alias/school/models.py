from django.db import models
from django.core.validators import RegexValidator

from django_countries.fields import CountryField


PHONE_REGEXP = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Inserire il numero nel formato: '+999999999'.")


class Contact(models.Model):
    address = models.CharField("Indirizzo", max_length=512)
    zip_code = models.CharField("CAP", max_length=5)
    country = CountryField("Nazione")
    phone_number = models.CharField("Telefono", validators=[PHONE_REGEXP], max_length=32, blank=True)
    fax = models.CharField("Fax", validators=[PHONE_REGEXP], max_length=32, blank=True)
    website = models.URLField("Sito web")
    email = models.EmailField("Email")

    class Meta:
        abstract = True


class Person(Contact):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField("Nome", max_length=128)
    last_name = models.CharField("Cognome", max_length=128)
    birth_date = models.DateField("Data di Nascita")
    birth_place = models.CharField(max_length=128)
    sex = models.CharField("Sesso", max_length=1, choices=GENDER_CHOICES)
    skype_id = models.CharField("Skype Id", max_length=64)


class Partner(Contact):
    name = models.CharField("Nome", max_length=256)
    vat = models.CharField("P.IVA", max_length=16)
    main_contact = models.ForeignKey("Person", verbose_name="Contatto principale")


class Lodge(Contact):
    landlord = models.ForeignKey("Person", verbose_name="Proprietario")
    link_to_map = models.URLField("Google Maps")
    # TODO: file field for mutliple pictures attachments


class Student(Person):
    notes = models.TextField("Note")
    academic = models.BooleanField("Accademico")
    partner_from = models.ForeignKey("Partner", verbose_name="Ente di provenienza")
    passport_number = models.CharField("Passaporto n.", max_length=16)
    # TODO: file field for mutliple generic attachment

    @property
    def italian(self):
        # TODO: FIXME
        return False


class CourseLevel(models.Model):
    name = models.CharField("Nome", max_length=32)
    description = models.TextField("Descrizione")


class Session(models.Model):
    TYPE_CHOICES = (
        ('intensivo', 'Intensivo'),
        ('semintensivo', 'Semintensivo'),
        ('ordinario', 'Ordinario'),
        ('individuale', 'Individuale')
    )
    name = models.CharField("Nome", max_length=256)
    type = models.CharField("Tipo", choices=TYPE_CHOICES, max_length=16)
    start = models.DateField("Data inizio")
    end = models.DateField("Data fine")
    duration = models.IntegerField("Durata in ore")
    description = models.TextField("Descrizione")
    level_in = models.ForeignKey("CourseLevel", verbose_name="Livello entrata", related_name="level_in")
    level_out = models.ForeignKey("CourseLevel", verbose_name="Livello uscita", related_name="level_out")
    course = models.ForeignKey("Course", verbose_name="Corso")


class CostItem(models.Model):
    name = models.CharField("Descrizione", max_length=32)
    amount = models.DecimalField("Costo", max_digits=6, decimal_places=2)


class Course(models.Model):
    notes = models.TextField("Note")
    student = models.ForeignKey("Student", verbose_name="Studente")
    cfu = models.IntegerField("CFU")
    invoice_to_partner_from = models.BooleanField("Fattura all'ente di provenienza")
    proforma_sent_on = models.DateTimeField("Data invio proforma")
    staying_confirm_sent_on = models.DateTimeField("Data invio conferma alloggio")

    @property
    def start_date(self):
        # FIXME
        return None

    @property
    def end_date(self):
        # FIXME
        return None

    @property
    def duration(self):
        # FIXME
        return None

    @property
    def individual_hours(self):
        # FIXME
        return 0

    @property
    def cost_items(self):
        # FIXME
        return []

    @property
    def cost(self):
        # FIXME
        return 0.0


class Staying(models.Model):
    date_from = models.DateField("Dal")
    date_to = models.DateField("Al")
    lodge = models.ForeignKey("Lodge", verbose_name="Alloggio")
    course = models.ForeignKey("Course", verbose_name="Corso")
