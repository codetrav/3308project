.. smartOBD documentation master file, created by
   sphinx-quickstart on Fri Nov 22 13:05:02 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to smartOBD's documentation!
====================================
smartOBD is a python module that uses ELM-347 OBD-II adapters to write data about a vehicle to a database, either in real-time using :mod:`asynco`, or in aggregate using :mod:`test_commands`.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Interface (Main function)
=========================

.. automodule:: smartOBD.main
   :members:

Adding a New Car
================

.. automodule:: smartOBD.new_car
   :members:
Also creates new car and car_temp table for :func:`smartOBD.test_commands.fullQuery()` and :func:`smartOBD.asynco.getAsync()`

Asynchronous Connections
========================

.. automodule:: smartOBD.asynco
   :members:

Inputs
 - Username (str) -- username in database
 - Car make/model (str, str) -- make and model of car desired if user has more than one car in the database


Full Query
==========

.. automodule:: smartOBD.test_commands
   :members: fullQuery

Parses through all OBDCommands as a dictionary, and queries the car with all commands,
appends results to a data array,
checks database for all columns and appends new ones,
finally, writes to database
.. code-block::
    # dictionary generation
    for key, i in test_dict.items():
        # print(key, test_dict[key])
        command.append((key, test_dict[key]))

    #basic loop for running commands from dictionary
    for i in range(0, len(temp2)):
    res = str((car.query(temp2[i])).value)
    description = str(temp2[i])
    if(res != 'None'):
        columns.append(description.rsplit(': ', 1)[1])
        results.append(str(res).rsplit(' ', 1)[0])


After running all queries, final column generation and insertion
.. code-block::
    # * length checking for all arrays
    if(len(columns) != len(results)):
        print("Results error")
    # *final loop for database access
    else:
        print("Parsing success")
        print(len(columns),"=",len(results))
        # * checking all columns for existence
        for i in range(1, len(columns)):
            data = columns[i]
            data = data.replace("'", " ")
            data = data.replace("\"", " ")
            cur.execute("select exists(select 1 from information_schema.columns where table_name='%s' and column_name='%s');",
                        (AsIs(dbtable), AsIs(data)))
            test = cur.fetchone()[0]
            if(not test):
                data.replace("'", " ")
                data.replace("\"", " ")
                cur.execute("alter table %s add column \"%s\" VARCHAR(2000)",
                            (AsIs(dbtable), AsIs(data)))
                print("TABLE ALTERED",data)
        # * final insertion
        dbconn.commit()
        q1 = sql.SQL("insert into {0} values ({1})").format(sql.Identifier(dbtable),
                                                            sql.SQL(', ').join(sql.Placeholder() * len(results)))
        # print(results)
        cur.execute(q1, results)
        dbconn.commit()
        print("Successful Read")

.. automodule:: smartOBD.test_commands
   :members: userGet
   :noindex: