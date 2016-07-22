hi default Member ctermfg=Cyan guifg=Cyan
hi default Variable ctermfg=Grey guifg=Grey
hi default Namespace ctermfg=Yellow guifg=#BBBB00
hi default Typedef ctermfg=Yellow gui=bold guifg=#BBBB00
hi default EnumConstant ctermfg=LightGreen guifg=LightGreen
hi default chromaticaException ctermfg=Yellow gui=bold guifg=#B58900
hi default chromaticaCast ctermfg=Green gui=bold guifg=#719E07
hi default OperatorOverload cterm=bold ctermfg=14 gui=bold guifg=#268bd2
hi default AccessQual cterm=underline ctermfg=81 gui=bold guifg=#6c71c4
hi default Linkage ctermfg=239 guifg=#09AA08
hi default AutoType ctermfg=Yellow guifg=#cb4b16

hi default link chromaticaPrepro PreProc
hi default link chromaticaDecl Identifier
hi default link chromaticaRef Type
hi default link chromaticaKeyword Keyword

hi default link chromaticaInclusionDirective cIncluded
hi default link chromaticaDeclRefExprEnum Constant
hi default link chromaticaDeclRefExprCall Type
hi default link chromaticaMemberRefExprCall Type
hi default link chromaticaMemberRefExprVar Type
hi default link chromaticaTemplateNoneTypeParameter Identifier

hi link chromaticaStructDecl Type
hi link chromaticaUnionDecl Type
hi link chromaticaClassDecl Type
hi link chromaticaEnumDecl Type
hi link chromaticaFieldDecl Member
hi link chromaticaEnumConstantDecl EnumConstant
hi link chromaticaFunctionDecl Function
hi link chromaticaVarDecl Variable
hi link chromaticaParmDecl Variable
hi link chromaticaObjCInterfaceDecl Normal
hi link chromaticaObjCCategoryDecl Normal
hi link chromaticaObjCProtocolDecl Normal
hi link chromaticaObjCPropertyDecl Normal
hi link chromaticaObjCIvarDecl Normal
hi link chromaticaObjCInstanceMethodDecl Normal
hi link chromaticaObjCClassMethodDecl Normal
hi link chromaticaObjCImplementationDecl Normal
hi link chromaticaObjCCategoryImplDecl Normal
hi link chromaticaTypedefDecl Type
hi link chromaticaCXXMethod Function
hi link chromaticaNamespace Namespace
hi link chromaticaLinkageSpec Normal
hi link chromaticaConstructor Function
hi link chromaticaDestructor Function
hi link chromaticaConversionFunction Function
hi link chromaticaTemplateTypeParameter Type
hi link chromaticaNonTypeTemplateParameter Variable
hi link chromaticaTemplateTemplateParameter Type
hi link chromaticaFunctionTemplate Function
hi link chromaticaClassTemplate Type
hi link chromaticaClassTemplatePartialSpecialization Type
hi link chromaticaNamespaceAlias Namespace
hi link chromaticaUsingDirective Type
hi link chromaticaUsingDeclaration Type
hi link chromaticaTypeAliasDecl Type
hi link chromaticaObjCSynthesizeDecl Normal
hi link chromaticaObjCDynamicDecl Normal
hi link chromaticaCXXAccessSpecifier Label
hi link chromaticaObjCSuperClassRef Normal
hi link chromaticaObjCProtocolRef Normal
hi link chromaticaObjCClassRef Normal
hi link chromaticaTypeRef Type
hi link chromaticaCXXBaseSpecifier Type
hi link chromaticaTemplateRef Type
hi link chromaticaNamespaceRef Namespace
hi link chromaticaMemberRef Member
hi link chromaticaLabelRef Label
hi link chromaticaOverloadedDeclRef Function
hi link chromaticaVariableRef Variable
hi link chromaticaFirstInvalid Normal
hi link chromaticaInvalidFile Error
hi link chromaticaNoDeclFound Error
hi link chromaticaNotImplemented Normal
hi link chromaticaInvalidCode Error
hi link chromaticaFirstExpr Normal
hi link chromaticaDeclRefExpr Variable
hi link chromaticaMemberRefExpr Member
hi link chromaticaCallExpr Function
hi link chromaticaObjCMessageExpr Normal
hi link chromaticaBlockExpr Normal
hi link chromaticaMacroDefinition Macro
hi link chromaticaMacroInstantiation Macro
hi link chromaticaIntegerLiteral Number
hi link chromaticaFloatingLiteral Float
hi link chromaticaImaginaryLiteral Number
hi link chromaticaStringLiteral String
hi link chromaticaCharacterLiteral Character
hi link chromaticaPunctuation Normal
hi link chromaticaIf Conditional
hi link chromaticaSwitch Conditional
hi link chromaticaLoop Repeat
hi link chromaticaStatement Statement
hi link chromaticaType Type
hi link chromaticaBoolean Boolean
hi link chromaticaConstant Constant
hi link chromaticaCXXCast chromaticaCast
hi link chromaticaCStyleCast chromaticaCast
hi link chromaticaExceptionStatement chromaticaException
hi link chromaticaExceptionAttr chromaticaException
hi link chromaticaTypeAliasStatement Statement
hi link chromaticaFile Namespace
hi link chromaticaIncludedHeaderFile Namespace
hi link chromaticaFinalAttr Statement
hi link chromaticaOverrideAttr Statement
hi link chromaitcaConstAttr Typedef
hi link chromaticaTypedef Typedef
hi link chromaticaStorageClass Statement
hi link chromaticaOperatorOverload OperatorOverload
hi link chromaticaAccessQual AccessQual
hi link chromaticaSpecifier Type
hi link chromaticaLinkage Linkage
hi link chromaticaAutoType Type
hi link chromaticaRegister Type
hi link chromaticaThreadLocal Type
hi link chromaticaRegister Type
hi link chromaticaRegister Type
hi link chromaticaConditionalOperator Todo
" Microsoft
hi link chromaticaMSStatement Statement

let b:chromatica_syntax_loaded = 1
