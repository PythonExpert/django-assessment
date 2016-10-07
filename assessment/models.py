# -*- coding: utf-8 -*-
import datetime
import uuid
from django.db import models
from django.conf import settings
from parler.models import TranslatableModel
from parler.models import TranslatedFields
from django.utils.translation import ugettext as _


class Survey(TranslatableModel):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    translations = TranslatedFields(
        name=models.CharField(_("name"), max_length=160),
        slug=models.SlugField(_("slug"), max_length=160, unique=True),
        description=models.TextField(_("description")),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
    )

    start_date_time = models.DateTimeField(
        _("start time"),
        auto_now=False,
        default=datetime.datetime.now,
    )

    end_date_time = models.DateTimeField(
        _("end time"),
        auto_now=False,
        null=True,
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assessment_surveys",
        verbose_name=_('owner'),
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _("survey")
        verbose_name_plural = _("surveys")

    def __str__(self):
        return self.name


class SurveyAdmin(models.Model):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("admin"),
    )

    survey = models.ForeignKey(
        Survey,
        verbose_name=_("survey"),
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _("survey admin")
        verbose_name_plural = _("survey admins")

    def __str__(self):
        try:
            return self.admin.username
        except Exception:
            return str(self.pk)


class SurveyGroup(models.Model):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    name = models.CharField(
        _("group name"),
        max_length=160,
    )

    surveys = models.ManyToManyField(
        Survey,
        blank=True,
        related_name='survey_groups',
        verbose_name=_("surveys"),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _("survey group")
        verbose_name_plural = _("survey groups")

    def __str__(self):
        return self.name


class Profile(models.Model):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="assessment_profile",
        verbose_name=_("user"),
    )

    surveys = models.ManyToManyField(
        Survey,
        blank=True,
        related_name='surveys',
        verbose_name=_("surveys"),
    )

    survey_groups = models.ManyToManyField(
        SurveyGroup,
        blank=True,
        related_name='survey_groups',
        verbose_name=_("survey groups"),
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        try:
            return self.user.get_full_name()
        except Exception:
            return str(self.pk)


class Question(TranslatableModel):

    TRUEFALSE = 1
    MULTIPLE_CHOICE = 2
    TEXT = 3

    QUESTION_TYPE = (
        (TRUEFALSE, _('true or false')),
        (MULTIPLE_CHOICE, _('multiple choice')),
        (TEXT, _('text')),
    )

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    translations = TranslatedFields(
        question=models.CharField(_("question"), max_length=512),
    )

    survey = models.ForeignKey(
        Survey,
        verbose_name=_("survey")
    )

    of_type = models.IntegerField(
        _("type"),
        choices=QUESTION_TYPE,
        default=TRUEFALSE,
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.question


class Choice(TranslatableModel):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    translations = TranslatedFields(
        value=models.CharField(_("value"), max_length=512),
    )

    question = models.ForeignKey(
        Question,
        related_name='choices',
        verbose_name=_("question"),
    )

    is_correct = models.BooleanField(
        _("correct"),
        default=False,
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _('choice')
        verbose_name_plural = _('choices')

    def __str__(self):
        return self.value


class Result(models.Model):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    timestamp = models.DateTimeField(
        editable=False,
        default=datetime.datetime.now,
    )

    survey = models.ForeignKey(
        Survey,
        editable=False,
        related_name='results',
        verbose_name=_("survey"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        related_name='results',
        verbose_name=_("user"),
    )

    class Meta:
        app_label = 'assessment'
        verbose_name = _('result')
        verbose_name_plural = _('results')
        unique_together = ('survey', 'user')

    def __str__(self):
        return str(self.pk)


class Answer(models.Model):

    _uid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    result = models.ForeignKey(
        Result,
        editable=False,
        related_name='answers',
        verbose_name=_("result"),
    )

    question = models.ForeignKey(
        Question,
        editable=False,
        related_name='answers',
        verbose_name=_("question"),
    )

    answer = models.TextField(
        _("answer"),
    )

    class Meta:
        app_label = 'assessment'
        unique_together = ('result', 'question')
        verbose_name = _('answer')
        verbose_name_plural = _('answers')

    def __str__(self):
        return self.answer
