"""
Copyright 2010, Kelsey Hightower
Kelsey Hightower <kelsey.hightower@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301  USA
"""

from past.builtins import str
from cobbler.items import item
from cobbler import utils
from cobbler.cexceptions import CX
from cobbler.utils import _


# this data structure is described in item.py
FIELDS = [
    # non-editable in UI (internal)
    ["ctime", 0, 0, "", False, "", 0, "int"],
    ["depth", 2, 0, "", False, "", 0, "float"],
    ["is_definition", False, 0, "Is Definition?", True, "Treat this class as a definition (puppet only)", 0, "bool"],
    ["mtime", 0, 0, "", False, "", 0, "int"],
    ["uid", "", 0, "", False, "", 0, "str"],

    # editable in UI
    ["class_name", "", 0, "Class Name", True, "Actual Class Name (leave blank to use the name field)", 0, "str"],
    ["comment", "", 0, "Comment", True, "Free form text description", 0, "str"],
    ["files", [], 0, "Files", True, "File resources", 0, "list"],
    ["name", "", 0, "Name", True, "Ex: F10-i386-webserver", 0, "str"],
    ["owners", "SETTINGS:default_ownership", "SETTINGS:default_ownership", "Owners", True, "Owners list for authz_ownership (space delimited)", 0, "list"],
    ["packages", [], 0, "Packages", True, "Package resources", 0, "list"],
    ["params", {}, 0, "Parameters/Variables", True, "List of parameters/variables", 0, "dict"],
]


class Mgmtclass(item.Item):

    TYPE_NAME = _("mgmtclass")
    COLLECTION_TYPE = "mgmtclass"

    def __init__(self, *args, **kwargs):
        super(Mgmtclass, self).__init__(*args, **kwargs)
        self.params = None

    #
    # override some base class methods first (item.Item)
    #

    def make_clone(self):

        _dict = self.to_dict()
        cloned = Mgmtclass(self.collection_mgr)
        cloned.from_dict(_dict)
        return cloned

    def get_fields(self):
        return FIELDS

    def check_if_valid(self):
        if not self.name:
            raise CX("name is required")

    #
    # specific methods for item.Mgmtclass
    #

    def set_packages(self, packages):
        self.packages = utils.input_string_or_list(packages)

    def set_files(self, files):
        self.files = utils.input_string_or_list(files)

    def set_params(self, params):
        (success, value) = utils.input_string_or_dict(params, allow_multiples=True)
        if not success:
            raise CX(_("invalid parameters"))
        else:
            self.params = value

    def set_is_definition(self, isdef):
        self.is_definition = utils.input_boolean(isdef)

    def set_class_name(self, name):
        if not isinstance(name, str):
            raise CX(_("class name must be a string"))
        for x in name:
            if not x.isalnum() and x not in ["_", "-", ".", ":", "+"]:
                raise CX(_("invalid characters in class name: '%s'" % name))
        self.class_name = name

# EOF
