# chromatica.nvim

Chromatica is an asynchronous syntax highlight engine for Neovim. It is a
python3 remote plugin. Currently, chromatica focuses on providing semantic
accurate syntax highlighting for C-family languages (using libclang).

This project is largely inspired by [deoplete][1] and [color_coded][2].

## Features

* Asynchronous parsing and highlighting provides fast and responsive highlight
  as you update your code.
* Semantic-accurate highlighting for C-family languages.

## Prerequites

* [Neovim][3]
* [Python3][4] and [Neovim python client][5]
* [libclang][6] (prefers 3.9.0, the latest HEAD version)

## Installation

### Install Prerequites

Install neovim python client and latest clang
```bash
pip3 install neovim
brew install llvm --HEAD --with-clang
```

### Install Chromatica

Use a plugin manager (for example, Neobundle)

```vim
NeoBundle 'arakashic/chromatica.nvim'
```

Or manually check out the repo and put the directory to your vim runtime path.


## Essential Settings

You need to set the path to your libclang

```vim
let g:chromatica#libclang_path='/usr/local/opt/llvm/lib'
```
The path can be set to either the path of the libclang.dylib/libclang.so file,
or the directory that contains it.

## `.clang` File and Compilation Database

## Responsive Mode

[1]: https://github.com/Shougo/deoplete.nvim
[2]: https://github.com/jeaye/color_coded
[3]: https://neovim.io
[4]: https://www.python.org/download/releases/3.0
[5]: https://github.com/neovim/python-client
[6]: http://clang.llvm.org
