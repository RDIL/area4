"""Runs code tests in a CI environment."""

# Import needed modules
import os
import restructuredtext_lint

# Try to import area4.
# This will fail if it could not be installed or if faulty code is present.
try:
    import area4
except ImportError:
    # At this point, area4 either isn't in site-packages,
    # or not on the system at all.
    raise OSError("Failed to import the library.")

# Create some variables that will be needed later.

# RAW_DIVIDERS is the array of dividers from the text file
RAW_DIVIDERS = None

# WORKING_DIRECTORY is the place that the tests are running in.
WORKING_DIRECTORY = None

# D is the area4 instance
D = None

# Determine if this is a tag build:
tag = (os.getenv("CIRRUS_TAG") is not None) and \
      (os.getenv("CIRRUS_TAG") != "")

# Get commit message:
COMMIT_MESSAGE = os.getenv("CIRRUS_CHANGE_MESSAGE")
if COMMIT_MESSAGE is None:
    raise EnvironmentError("No commit name detected!")

# Get the branch:
REPO_BRANCH = os.getenv("CIRRUS_BRANCH")
if REPO_BRANCH is None:
    raise EnvironmentError("Branch unknown")

# Get the target:
TARGET = os.getenv("TARGET")

# Make the fetched values lowercase:
COMMIT_MESSAGE = COMMIT_MESSAGE.lower()
REPO_BRANCH = REPO_BRANCH.lower()
if TARGET is not None:
    TARGET = TARGET.lower()

# Check if extra tests should be run:
EXTRA_TESTS = False


# Function to send debug messages to the console:
def debug(message):
    """
    Log a debug message.

    :return: None
    :param message: the message to log
    """
    print("{0}{1}{2}{3}".format("[Verbose]", " ", message, "."))


# Make sure this is being run directly, and
# not from another python module:
if __name__ != "__main__":
    raise EnvironmentError("This module must be run directly!")
else:
    # If this is being run directly, set up for tests:
    debug("Module being run directly, not exiting")
    # Get working directory:
    debug("Getting working directory")
    WORKING_DIRECTORY = os.getenv("CIRRUS_WORKING_DIR")
    debug("Got working directory ({0})".format(WORKING_DIRECTORY))
    # Get divider text file:
    DIVIDERS_FILE = "{0}/{1}".format(WORKING_DIRECTORY, "area4/dividers.txt")
    debug("Divider file is located at {0}".format(DIVIDERS_FILE))
    with open(DIVIDERS_FILE, mode="r") as fh:
        RAW_DIVIDERS = fh.readlines()
        debug("Fetched raw dividers text file")
    # Create instance:
    debug("Creating instance of the library")
    D = area4.Area4Instance()
    debug("Created instance")

    # See if we need to run extra tests:
    if ("!e" in COMMIT_MESSAGE or COMMIT_MESSAGE == "!e") or \
            (REPO_BRANCH == "master") or \
            tag:
        debug("Running extra tests")
        EXTRA_TESTS = True
    else:
        EXTRA_TESTS = False


def test_dividers():
    """
    Test each divider against the raw ones from the text file.

    :return: None
    """
    for i, item in enumerate(RAW_DIVIDERS):
        if i < 1 or i == 35:
            debug("Manually skipping divider {0}".format(i))
            # Manually skip dividers 0 and 35:
            i = i + 1
        else:
            debug("Testing divider {0}".format(i))
            try:
                # Try to match the raw divider with the result
                # of the function:
                if RAW_DIVIDERS[i].split("\n")[0] == D.divider(i):
                    debug("[+] Divider {0} should work".format(i))
                else:
                    debug("[X] Divider {0} is broken".format(i))
                    raise RuntimeError("Broken divider detected!")
            except IndexError:
                # This is thrown if a number is offset in the divider array.
                # What we do about it is we just simply ignore it
                debug("Ignoring an IndexError")


def test_make_div():
    """
    Tests the make-div function.

    :return: None
    """
    if D.make_div('=-', length=9, start='<', end='=>') == "<=-=-=-=>":
        debug("make-div test did not fail")
    else:
        raise RuntimeError("make-div tests failed")


def testLogDivider() -> None:
    """
    Test LogDivider.

    :return None:
    """
    print("[DEBUG] Running logDivider tests")
    compare1 = D.splitter("---", "Hello") == "Hello"
    if not compare1:
        raise RuntimeError("Test failed")
    else:
        print("\n[DEBUG] Test of LogDivider passed")


def test_info():
    """
    Tests the info variables. This is an extra test.

    :return: None
    """
    right_data = [
        "area4",
        "https://github.com/RDIL",
        "me@rdil.rocks",
        "support@rdil.rocks",
        "Dividers in Python, the easy way!"
    ]
    from_class = [
        D.name,
        D.author,
        D.author_email,
        D.support_email,
        D.description
    ]
    debug("Running extra test for package info")
    for the_location, place_holder in enumerate(right_data):
        if not right_data[the_location] == from_class[the_location]:
            raise RuntimeError("[X] Failed package info test {0}"
                               .format(the_location)
                               )
        else:
            debug("[+] Data item {0} works".format(the_location))


def rst_lint_run():
    """
    Lints all reStructuredText files. This is an extra check.

    :return: None
    """
    debug("Running reStructuredText linting")
    files = os.listdir("{0}/docs".format(WORKING_DIRECTORY))
    for name in files:
        path = "{0}/docs/{1}".format(WORKING_DIRECTORY, name)
        restructuredtext_lint.lint_file(filepath=path)


def markdown_tests_run():
    """
    Run markdown lint and link check.

    :return: None
    """
    debug("Running markdown tests")
    files1 = os.listdir(WORKING_DIRECTORY)
    files2 = os.listdir("{0}/.github".format(WORKING_DIRECTORY))
    files3 = os.listdir("{0}/.github/ISSUE_TEMPLATE".format(
        WORKING_DIRECTORY)
    )
    files4 = os.listdir("{0}/extras".format(WORKING_DIRECTORY))
    for name in files1:
        if name.__contains__(".md"):
            path = "{0}/{1}".format(WORKING_DIRECTORY, name)
            os.system("markdown-link-check {0}".format(path))
            os.system("markdownlint --config=.markdownlint.yml {0}".
                      format(path))
    for name in files2:
        if name.__contains__(".md"):
            path = "{0}/.github/{1}".format(WORKING_DIRECTORY, name)
            os.system("markdown-link-check {0}".format(path))
            os.system("markdownlint --config=.markdownlint.yml {0}".
                      format(path))
    for name in files3:
        if name.__contains__(".md"):
            path = "{0}/.github/ISSUE_TEMPLATE/{1}".format(
                WORKING_DIRECTORY, name
            )
            os.system("markdown-link-check {0}".format(path))
            os.system("markdownlint --config=.markdownlint.yml {0}".
                      format(path))
    for name in files4:
        if name.__contains__(".md"):
            path = "{0}/extras/{1}".format(WORKING_DIRECTORY, name)
            os.system("markdown-link-check {0}".format(path))
            os.system("markdownlint --config=.markdownlint.yml {0}".
                      format(path))


def safety_run():
    """
    Run SafetyCI by PyUp.

    :return: None
    """
    os.system("make safetyci")


if TARGET == "code":
    # Run tests:
    test_dividers()
    test_make_div()
    testLogDivider()
    if EXTRA_TESTS:
        # Run extra tests if needed:
        test_info()
        rst_lint_run()
        safety_run()
elif TARGET == "markdown":
    markdown_tests_run()

debug("Finished tests")
