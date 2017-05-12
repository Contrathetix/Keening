# Python imports
import sys

# Keening imports
import Modules.ApplicationCore as ApplicationCore


if __name__ == '__main__':
    app = ApplicationCore.ApplicationCore(sys.argv)
    sys.exit(app.exec_())
