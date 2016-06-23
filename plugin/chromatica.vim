" ============================================================================
" FILE: chromatica.py
" AUTHOR: Yanfei Guo <yanf.guo at gmail.com>
" License: MIT license
" ============================================================================
"
if exists('g:loaded_chromatica')
    finish
endif

if get(g:, 'chromatica#enable_at_startup', 0) && !exists('#chromatica') "{{{
    call chromatica#enable()
    " augroup chromatica
    "     autocmd CursorHold * call chromatica#enable()
    "     autocmd InsertEnter * call chromatica#enable()
    "                 \ | silent! doautocmd <nomodeline> chromatica InsertEnter
    " augroup END
endif "}}}

if get(g:, 'chromatica#enable_debug', 0) && !exists('#chromatica') "{{{
    call chromatica#enable_logging('DEBUG', 'chromatica.log')
endif "}}}

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )
execute('source '. s:script_folder_path . '/../syntax/chromatica.vim')

let g:loaded_chromatica=1

