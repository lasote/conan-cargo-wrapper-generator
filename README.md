# Conan cargo wrapper generator

If you are writting some Rust wrapper for a C library that is uploaded to **conan** you can use this generator to write a Rust build script containing all the paths/lib names required to link with. You can see a real example in my fork of rust-openssl wrapper (https://github.com/lasote/rust-openssl/tree/master/openssl-sys)

## How to use

Write a conanfile.txt file and specify the required libraries and the current generator:

```
[requires]
ConanCargoWrapper/0.1@lasote/stable
OpenSSL/1.0.2h@lasote/stable

[generators]
ConanCargoWrapper

```

- Run conan install command, this will generate a file named **conan_cargo_build.rs** with the needed information to link against the required libraries:

```
$ conan install
```

**conan_cargo_build.rs**

This file contains a main() function that prints the "cargo:" variables needed to link with the specified conan package, furthermore, it define some constants if you want to import this module and play with the variables:

```
  
fn main() {
    println!("cargo:rustc-link-search=native=/home/laso/.conan/data/OpenSSL/1.0.2h/lasote/stable/package/735a582f7a1ccadcb2b9c7e7f9cdec974e938950/lib");
    println!("cargo:rustc-link-search=native=/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/lib");
    println!("cargo:rustc-link-lib=ssl");
    println!("cargo:rustc-link-lib=crypto");
    println!("cargo:rustc-link-lib=dl");
    println!("cargo:rustc-link-lib=z");
    println!("cargo:include=/home/laso/.conan/data/OpenSSL/1.0.2h/lasote/stable/package/735a582f7a1ccadcb2b9c7e7f9cdec974e938950/include");
    println!("cargo:include=/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/include");
}

pub const LIB_PATHS: &'static [ &'static str ] = &["/home/laso/.conan/data/OpenSSL/1.0.2h/lasote/stable/package/735a582f7a1ccadcb2b9c7e7f9cdec974e938950/lib", "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/lib"];
pub const LIBS: &'static [ &'static str ] = &["ssl", "crypto", "dl", "z"];
pub const INCLUDE_PATHS: &'static [ &'static str ] = &["/home/laso/.conan/data/OpenSSL/1.0.2h/lasote/stable/package/735a582f7a1ccadcb2b9c7e7f9cdec974e938950/include", "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/include"];

```

-  Edit your **Cargo.toml** file and specify the build script to "conan_cargo_build.rs":

```

[package]
name = "examplelib"
version = "0.1.2"
authors = ["Luis Martinez de Bartolome <lasote@gmail.com>"]
license = "MIT"
description = "Test package"
links = "openssl"
build = "conan_cargo_build.rs"

```

- You could also use your own **build.rs** file and import the **conan_cargo_build** to use the defined constants.

- Build and test your cargo package as always:


```
cargo clean
cargo build
cargo test
```

