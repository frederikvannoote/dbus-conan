from conans import ConanFile, CMake, tools

class DBusConan(ConanFile):
    name = "dbus"
    version = "1.13.18"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"

    options = { "win_service": [True, False] }
    default_options = { "win_service": False }
    
    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt"

    generators = "cmake_find_package"
    
    requires = (
        "expat/2.4.1"
    )
    
    def config_options(self):
        self.options["expat"].shared = True
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        git = tools.Git(folder=".")
        git.clone("https://gitlab.freedesktop.org/dbus/dbus.git", "dbus-1.13.18")

    def build(self):
        if self.options.win_service == True:
            tools.patch(patch_file="bus-service-win.patch")
        cmake = CMake(self)
        cmake.definitions["DBUS_ENABLE_XML_DOCS"] = "OFF"
        cmake.configure(source_folder=".")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["dbus"]
