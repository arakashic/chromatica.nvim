" ============================================================================
" FILE: chromatica.py
" AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
" License: MIT license
" ============================================================================
"
if exists('g:loaded_chromatica')
    finish
endif

if get(g:, 'chromatica#enable_at_startup', 0) "{{{
    augroup chromatica
        autocmd VimEnter * call chromatica#enable()
    augroup END
endif "}}}

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )
execute('source '. s:script_folder_path . '/../syntax/chromatica.vim')

command! ChromaticaStart call chromatica#enable()
command! ChromaticaStop call chromatica#disable()
command! ChromaticaToggle call chromatica#toggle()
command! ChromaticaLogInfo call chromatica#enable_logging('INFO', 'chromatica.log')

command! PrintHL call chromatica#handlers#_print_highlight()

let g:loaded_chromatica=1

