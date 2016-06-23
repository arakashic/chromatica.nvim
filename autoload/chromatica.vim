" =============================================================================
" File: chromatica.vim
" Author: Yanfei Guo <yanf.guo at gmail.com>
" Last Modified: June 18, 2016
" License: MIT License
" based on original version by Shougo Matsushita <Shougo.Matsu at gmail.com>
" =============================================================================

function! chromatica#initialize() abort
    return chromatica#init#_initialize()
endfunction

function! chromatica#enable() abort
    if chromatica#initialize()
        return 1
    endif
    return chromatica#init#_enable()
endfunction

function! chromatica#disable() abort
    return chromatica#init#_disable()
endfunction

function! chromatica#toggle() abort
    return chromatica#init#_is_enabled() ? chromatica#disable() : chromatica#enable()
endfunction

function! chromatica#enable_logging(level, logfile) abort
    " Enable to allow logging before completions start.
    if chromatica#initialize()
        return
    endif

    call rpcrequest(g:chromatica#_channel_id,
                \ 'chromatica_enable_logging', a:level, a:logfile)
endfunction

" vim: tw=120:foldmarker={{{,}}}:foldmethod=marker:
