from conans import ConanFile, AutoToolsBuildEnvironment, tools
import sys
import shutil


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
        with tools.chdir("libsndfile"):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure()
            autotools.make()

    def package(self):
        self.copy("sndfile.h", dst="include", src="libsndfile/src")
        self.copy("sndfile.hh", dst="include", src="libsndfile/src")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["sndfile"]

