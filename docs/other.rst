Other Functions
===============

This is a list of other functions you may want to use, and what the do in basic terms.

See the API Refrence page for more information.

Splitter
--------

* :meth:`area4.splitter`

.. versionadded:: 2.1.0

The splitter function takes a string or number as a divider,
and a series of strings to return, divided.
If the first parameter is a number, it looks it up in the divider list.
Otherwise, it uses the string provided as a divider.
If only one additional string is provided, nothing is returned.

For example:

.. code-block:: python

    import area4
    print(area4.splitter(1, "Welcome to", "My **app**"))
    
    # outputs:
    # Welcome to
    # ------------
    # My **app**


Get Divider Character
---------------------

* :meth:`area4.utils.get_divider_character`

.. versionadded:: 2.1.7

Gets you the material, or character the divider is made of.
You need to pass an integer of the divider you want to get
the character it is made of.

For example:

.. code-block:: python

    from area4.util import get_divider_character

    print(get_divider_character(7))

    # This example prints a single equal sign to the console,
    # because that divider is '============'

Reddit Horizontal
-----------------

* :meth:`area4.utils.reddit_horizontal`

.. versionadded:: 2.3.1

This function returns the Reddit Markdown divider (for Reddit bots).
This function takes no parameters.

Markdown Horizontal
-------------------

* :meth:`area4.utils.markdown_horizontal`

.. versionadded:: 2.9.0

This function returns the Markdown divider
(rendered as an HTML 'hr' tag by sites like GitHub).
This function takes no parameters.

.. note::
    If you want the HTML tag equivalent of the rendered output,
    see :ref:`HTML Horizontal`.

HTML Horizontal
---------------

* :meth:`area4.utils.html_horizontal`

.. versionadded:: 3.1.0

This function returns the HTML tag(s) for the divider
element (rendered as a literal line by default, unless changed
via CSS).
This function takes 1 optional parameter, :code:`closing_tag`,
more information is detailed in the API Reference section.
