from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibsndfileConan(ConanFile):
    name = "libsndfile"
    version = "1.0.28"
    license = ("LGLP-2.1", "LGPL-3.0")
    author = "Martin Delille <martin@phonations.com>"
    url = "https://github.com/Phonations/conan-libsndfile"
    homepage = "http://www.mega-nerd.com/libsndfile"
    description = "A C library for reading and writing sound files containing sampled audio data."
    topics = ("audio", "sound", "wav", "aiff", "sampled-sound")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _autotools = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.clear()

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os == "Windows":
            del self.settings.build_type
            del self.settings.compiler

    def source(self):
        source_sha256 = "1ff33929f042fa333aed1e8923aa628c3ee9e1eb85512686c55092d1e5a9dfa9"
        extracted_folder = self.name + '-' + self.version
        url = "{}/files/{}".format(self.homepage, extracted_folder)
        tools.get("{}.tar.gz".format(url), sha256=source_sha256)
        os.rename(extracted_folder, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            args = [
                ("--enable-shared" if self.options.shared else "--enable-static"),
                ("--disable-static" if self.options.shared else "--disable-shared"),
                "--disable-sqlite",
                "--disable-alsa",
                "--disable-external-libs"
            ]
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(configure_dir=self._source_subfolder, args=args)
        return self._autotools

    def build(self):
        if self.settings.os == "Windows":
            archs = {"x86": "w32", "x86_64": "w64"}
            checksums = {
                "x86": "a73e1a8f87207e121a78e7cfbfe758d3ad15a28a37e4ca0e96d43348d53a2a1f",
                "x86_64": "b885e97c797c39127d7d252be0da704a8bbdb97948b562d95cd5b8821d2b42ba"
            }
            extracted_folder = self.name + '-' + self.version + '-' + archs[str(self.settings.arch)]
            url = "{}/files/{}".format(self.homepage, extracted_folder)
            tools.get("{}.zip".format(url), sha256=checksums[str(self.settings.arch)])
        else:
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", src="bin")
            self.copy("*.lib", dst="lib", src="lib")
            self.copy("*.h", dst="include", src="include")
            self.copy("*.hh", dst="include", src="include")
        else:
            autotools = self._configure_autotools()
            autotools.install()
            tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = ["sndfile"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("m")

