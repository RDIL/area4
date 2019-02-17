Using
=====

After you install the package (instructions in the installing section), you need to import it into any Python file that you will use it in.

You can do this by adding the following line to the top:

.. code-block:: python

    import area4

After doing so, you need to create an instance of the class, for example:

.. code-block:: python

    instanceName = area4.Area4Instance()

(replace instanceName with whatever you want, but do NOT use "area4" or "Area4")

.. warning:: Legacy versions don't work with the new methods. For old documentation, select 'v: stable' and then click 'legacy'.

And if you want to you can check to make sure the library is working:

.. code-block:: python

    print(instanceName.area4info())

.. warning:: The area4info function will only work on Python 3.6 or above.  Keep this in mind if using it and you don't want SyntaxErrors!  

Now, to get dividers, use this function:

.. code-block:: python

    print(
        instanceName.divider(4)
    )  # This example prints divider number 4 to the console

For what all the dividers look like, see the next section!  
