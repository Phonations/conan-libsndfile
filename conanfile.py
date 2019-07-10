from conans import ConanFile, CMake, tools
import sys


class LibsndfileConan(ConanFile):
    name = "libsndfile"
    version = "1.0.28"
    license = "<Put the package license here>"
    author = "Martin Delille <martin@phonations.com>"
    url = "https://github.com/Phonations/conan-libsndfile"
    description = "A C library for reading and writing sound files containing sampled audio data."
    topics = ("audio")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        url = "http://www.mega-nerd.com/libsndfile/files/libsndfile-{0}"\
            .format(self.version)
        if tools.os_info.is_windows:
            tools.get("%s-w64.zip" % url)
        elif sys.version_info.major >= 3:
            tools.get("%s.tar.gz" % url)
        else:  # python 2 cannot deal with .xz archives
            self.run("wget -qO- %s.tar.gz | tar -xJ " % url)
        shutil.move("libsndfile-%s" % self.version, "libsndfile")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="hello")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

