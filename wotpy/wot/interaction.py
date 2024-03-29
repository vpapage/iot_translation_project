#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classes that represent all interaction patterns.
"""

from abc import ABCMeta, abstractmethod

# noinspection PyPackageRequirements
from slugify import slugify

from wotpy.codecs.enums import MediaTypes
from wotpy.wot.enums import InteractionTypes
from wotpy.wot.validation import is_valid_safe_name
from wotpy.wot.dictionaries.interaction import PropertyFragmentDict, ActionFragmentDict, EventFragmentDict
from wotpy.wot.form import Form


class InteractionPattern(metaclass=ABCMeta):
    """A functionality exposed by Thing that is defined by the TD Interaction Model."""

    def __init__(self, thing, name, init_dict=None, **kwargs):
        if not is_valid_safe_name(name):
            raise ValueError("Invalid Interaction name: {}".format(name))

        self._init_dict = init_dict if init_dict else self.init_class(**kwargs)

        self._thing = thing
        self._name = name
        self._autogenerated_forms = []
        self._td_forms = []
        if self._init_dict.forms:
            self._td_forms = [
                Form(
                    interaction=self,
                    protocol=None,
                    href=form_input.href,
                    content_type=MediaTypes.JSON,
                    op=form_input.op)
                for form_input in self._init_dict.forms
            ]

    def __getattr__(self, name):
        """Search for members that raised an AttributeError in
        the private init dict before propagating the exception."""

        return getattr(self._init_dict, name)

    @property
    @abstractmethod
    def init_class(self):
        """Returns the init dict class for this type of interaction."""

        raise NotImplementedError()

    @property
    def interaction_fragment(self):
        """The InteractionFragment dictionary of this interaction."""

        return self._init_dict

    @property
    def thing(self):
        """Thing that contains this Interaction."""

        return self._thing

    @property
    def name(self):
        """Interaction name.
        No two Interactions with the same name may exist in a Thing."""

        return self._name

    @property
    def url_name(self):
        """URL-safe version of the name."""

        return slugify(self.name)

    @property
    def forms(self):
        """Sequence of forms linked to this interaction."""

        return self._td_forms + self._autogenerated_forms

    def clean_forms(self):
        """Removes all autogenerated Forms from this Interaction."""

        self._autogenerated_forms = []

    def add_form(self, form):
        """Add a new autogenerated Form."""

        assert form.interaction is self

        existing = next((True for item in self._autogenerated_forms if item.id == form.id), False)

        if existing:
            raise ValueError("Duplicate Form: {}".format(form))

        self._autogenerated_forms.append(form)

    def remove_form(self, form):
        """Remove an existing autogenerated Form."""

        try:
            pop_idx = self._autogenerated_forms.index(form)
            self._autogenerated_forms.pop(pop_idx)
        except ValueError:
            pass


class Property(InteractionPattern):
    """Properties expose internal state of a Thing that can be
    directly accessed (get) and optionally manipulated (set)."""

    @property
    def init_class(self):
        """Returns the init dict class for this type of interaction."""

        return PropertyFragmentDict

    @property
    def interaction_type(self):
        """Interaction type."""

        return InteractionTypes.PROPERTY


class Action(InteractionPattern):
    """Actions offer functions of the Thing. These functions may manipulate the
    internal state of a Thing in a way that is not possible through setting Properties."""

    @property
    def init_class(self):
        """Returns the init dict class for this type of interaction."""

        return ActionFragmentDict

    @property
    def interaction_type(self):
        """Interaction type."""

        return InteractionTypes.ACTION


class Event(InteractionPattern):
    """The Event Interaction Pattern describes event sources that asynchronously push messages.
    Here not state, but state transitions (events) are communicated (e.g., clicked)."""

    @property
    def init_class(self):
        """Returns the init dict class for this type of interaction."""

        return EventFragmentDict

    @property
    def interaction_type(self):
        """Interaction type."""

        return InteractionTypes.EVENT
