rem
===
A simple CLI to-do list program. Create categories, tasks and detailed
explanations. Uses SQLite to store the data.

See [Usage examples](https://github.com/haukurpallh/rem#usage-examples) for an
overview of the features.

Setup
-----
### Installing on Linux
Open a terminal and execute the following commands (simply copy & paste):

    git clone git://github.com/haukurpallh/rem.git
    mv rem ~/.rem
    chmod +x ~/.rem/rem.py
    sudo ln -s ~/.rem/rem.py

That's all!


Usage examples
--------------

To create a new category (possibly with a task and details), execute `rem -a`
(or `rem -a CATEGORY_NAME` if you wish to specify the name of the category).
You will be prompted for the name of a task and afterwards for details. Neither
is necessary. Examples (the "$" sign is just to indicate it's a command, don't
type it):

    $ rem -a
    Enter a descriptive title for the task: test
    Enter a detailed description: some description

And:

    $ rem -a some_category
    Enter a descriptive title for the task: some_title
    Enter a detailed description: sleep, some_description

Now, to view the contents of the database we can run `rem -l` to list all the
categories and their tasks or `rem -l CATEGORY_NAME` to list only a specific
category. Examples (one for each of the examples above):

    $ rem -l
    General
      - Test
        Some description

    Some_category
      - Some_title
        Some_description

And:

    rem -l general
    General
      - Test
        Some description

To remove a the entire database, use the command `rem -r` and confirm. To
remove a single category, use `rem -r CATEGORY_NAME`. To remove more than one
category at once, separate them with a single comma. Examples:

    $ rem -r
    Permanently remove all data from the database (y/n)? n
    $ rem -l
    General
      - Test
        Some description

    Some_category
      - Some_title
        Some_description

And:

    $ rem -r general,some_category
    $ rem -l
    General

As you can see, the program automatically creates a category called general
even though it was just deleted.

For more help, try executing `rem -h`.

Note: the "merge" (-m, --merge) option is available even though -h lists it.
