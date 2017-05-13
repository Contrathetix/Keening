"""Main file to be executed."""

# Python imports
import sys

# Keening imports
import Common.Application as AppModule


if __name__ == '__main__':
    app = AppModule.Application(sys.argv)
    sys.exit(app.exec_())
