from conans.model import Generator
from conans.paths import BUILD_INFO
from conans import ConanFile, CMake


class ConanCargoWrapper(Generator):
    
    @property
    def filename(self):
        return "conan_cargo_build.rs"

    @property
    def content(self):
        template = '''
  
fn main() {
}

pub const LIB_PATHS: &'static [ &'static str ] = &[%(lib_paths)s];
pub const LIBS: &'static [ &'static str ] = &[%(libs)s];
pub const INCLUDE_PATHS: &'static [ &'static str ] = &[%(include_paths)s];
'''
        def append_to_template(line):
            return template.replace("}", "    %s\n}" % line)
        
        def comma_separate(list):
            return ", ".join(['r#"%s"#' % x for x in list])

        for lib_path in self.deps_build_info.lib_paths:
            new = 'println!(r#"cargo:rustc-link-search=native=%s"#);' % lib_path;
            template = append_to_template(new)
            
        for lib in self.deps_build_info.libs:
            new = 'println!(r#"cargo:rustc-link-lib=%s"#);' % lib;
            template = append_to_template(new)
        
        for lib in self.deps_build_info.include_paths:
            new = 'println!(r#"cargo:include=%s"#);' % lib;
            template = append_to_template(new)
            
        template = template % {"lib_paths": comma_separate(self.deps_build_info.lib_paths),
                               "libs": comma_separate(self.deps_build_info.libs) ,
                               "include_paths": comma_separate(self.deps_build_info.include_paths)  }
        
        return template


class CargoGeneratorPackage(ConanFile):
    name = "ConanCargoWrapper"
    version = "0.1"
    url = "https://github.com/lasote/conan-cargo-wrapper"
    license = "MIT"
    settings = None

    def build(self):
      pass

    def package_info(self):
      self.cpp_info.includedirs = []
      self.cpp_info.libdirs = []
      self.cpp_info.bindirs = []
