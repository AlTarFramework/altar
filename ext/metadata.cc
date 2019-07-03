// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// (c) 2010-2019 california institute of technology
// all rights reserved
//

#include <portinfo>
#include <Python.h>

#include "metadata.h"

// copyright
const char * const altar::extensions::copyright__name__ = "copyright";
const char * const altar::extensions::copyright__doc__ = "the module copyright string";
PyObject *
altar::extensions::
copyright(PyObject *, PyObject *)
{
    // the note
    const char * const copyright_note =
        "altar.beta: (c) 2013-2019 ParaSim Inc; 2010-2019 California Institute of Technology";
    // turn it into a python string
    return Py_BuildValue("s", copyright_note);
}


// license
const char * const altar::extensions::license__name__ = "license";
const char * const altar::extensions::license__doc__ = "the module license string";
PyObject *
altar::extensions::
license(PyObject *, PyObject *)
{
    const char * const license_string =
        "\n"
        "    altar 2.0\n"
        "    Copyright (c) 2013-2019 ParaSim Inc.\n"
        "    Copyright (c) 2010-2019 California Institute of Technology\n"
        "    All Rights Reserved\n"
        "\n"
        "\n"
        "    Redistribution and use in source and binary forms, with or without\n"
        "    modification, are permitted provided that the following conditions\n"
        "    are met:\n"
        "\n"
        "    * Redistributions of source code must retain the above copyright\n"
        "      notice, this list of conditions and the following disclaimer.\n"
        "\n"
        "    * Redistributions in binary form must reproduce the above copyright\n"
        "      notice, this list of conditions and the following disclaimer in\n"
        "      the documentation and/or other materials provided with the\n"
        "      distribution.\n"
        "\n"
        "    * Neither the name \"altar\" nor the names of its contributors may be\n"
        "      used to endorse or promote products derived from this software\n"
        "      without specific prior written permission.\n"
        "\n"
        "    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n"
        "    \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n"
        "    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS\n"
        "    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE\n"
        "    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,\n"
        "    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,\n"
        "    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"
        "    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER\n"
        "    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT\n"
        "    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN\n"
        "    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE\n"
        "    POSSIBILITY OF SUCH DAMAGE.\n";

    return Py_BuildValue("s", license_string);
}


// version
const char * const altar::extensions::version__name__ = "version";
const char * const altar::extensions::version__doc__ = "the module version string";
PyObject *
altar::extensions::
version(PyObject *, PyObject *)
{
    const char * const version_string = "2.0";
    return Py_BuildValue("s", version_string);
}


// end of file
