
from chromatica import logger
from chromatica.util import load_external_module

load_external_module(__file__, "")
from clang import cindex

log = logger.logging.getLogger("chromatica")

def get_cursor(tu, filename, row, col):
    return cindex.Cursor.from_location(tu, \
        cindex.SourceLocation.from_position(tu, tu.get_file(filename), row, col))

def get_symbol(cursor):
    """docstring for get_symbol"""
    if cursor.kind == cindex.CursorKind.MACRO_DEFINITION:
        return cursor

    symbol = cursor.get_definition()
    if not symbol:
        symbol = cursor.referenced

    if not symbol:
        return None

    if symbol.kind == cindex.CursorKind.CONSTRUCTOR \
            or symbol.kind == cindex.CursorKind.DESTRUCTOR:
        symbol = symbol.semantic_parent

    return symbol

def get_symbol_from_loc(tu, filename, row, col):
    """docstring for get_symbol_from_loc"""
    cursor = get_cursor(tu, filename, row, col)

    if not cursor:
        return None
    tokens = cursor.get_tokens()
    for token in tokens:
        # if token.kind.value == 2 \
        #         and row == token.location.line \
        if row == token.location.line \
                and token.location.column <= col \
                and col < token.location.column + len(token.spelling):
            symbol = get_symbol(cursor)
            if symbol and symbol.spelling == token.spelling:
                return symbol
    return None

LITERAL_GROUP = {
    cindex.CursorKind.INTEGER_LITERAL: "Number",
    cindex.CursorKind.FLOATING_LITERAL: "Float",
    cindex.CursorKind.IMAGINARY_LITERAL: "Number",
    cindex.CursorKind.STRING_LITERAL: "cidx.string",
    cindex.CursorKind.CHARACTER_LITERAL: "Character",
    cindex.CursorKind.OBJC_STRING_LITERAL: "cidx.objc_stiring_literal",
}

TYPE_GROUP = {
    cindex.TypeKind.UNEXPOSED: "Variable",
    cindex.TypeKind.VOID: "Variable",
    cindex.TypeKind.BOOL: "Variable",
    cindex.TypeKind.CHAR_U: "Variable",
    cindex.TypeKind.UCHAR: "Variable",
    cindex.TypeKind.CHAR16: "Variable",
    cindex.TypeKind.CHAR32: "Variable",
    cindex.TypeKind.USHORT: "Variable",
    cindex.TypeKind.UINT: "Variable",
    cindex.TypeKind.ULONG: "Variable",
    cindex.TypeKind.ULONGLONG: "Variable",
    cindex.TypeKind.UINT128: "Variable",
    cindex.TypeKind.CHAR_S: "Variable",
    cindex.TypeKind.SCHAR: "Variable",
    cindex.TypeKind.WCHAR: "Variable",
    cindex.TypeKind.SHORT: "Variable",
    cindex.TypeKind.INT: "Variable",
    cindex.TypeKind.LONG: "Variable",
    cindex.TypeKind.LONGLONG: "Variable",
    cindex.TypeKind.INT128: "Variable",
    cindex.TypeKind.FLOAT: "Variable",
    cindex.TypeKind.DOUBLE: "Variable",
    cindex.TypeKind.LONGDOUBLE: "Variable",
    cindex.TypeKind.NULLPTR: "Variable",
    cindex.TypeKind.OVERLOAD: "Variable",
    cindex.TypeKind.DEPENDENT: "Variable",
    cindex.TypeKind.OBJCID: "Variable",
    cindex.TypeKind.OBJCCLASS: "Variable",
    cindex.TypeKind.OBJCSEL: "Variable",
    cindex.TypeKind.COMPLEX: "Variable",
    cindex.TypeKind.POINTER: "Variable",
    cindex.TypeKind.BLOCKPOINTER: "Variable",
    cindex.TypeKind.LVALUEREFERENCE: "Variable",
    cindex.TypeKind.RVALUEREFERENCE: "Variable",
    cindex.TypeKind.RECORD: "Variable",
    cindex.TypeKind.TYPEDEF: "Variable",
    cindex.TypeKind.OBJCINTERFACE: "Variable",
    cindex.TypeKind.OBJCOBJECTPOINTER: "Variable",
    cindex.TypeKind.CONSTANTARRAY: "Variable",
    cindex.TypeKind.VECTOR: "Variable",
    cindex.TypeKind.INCOMPLETEARRAY: "Variable",
    cindex.TypeKind.VARIABLEARRAY: "Variable",
    cindex.TypeKind.DEPENDENTSIZEDARRAY: "Variable",
    cindex.TypeKind.AUTO: "Variable",
    cindex.TypeKind.MEMBERPOINTER: "Member",
    cindex.TypeKind.ENUM: "EnumConstant",
    cindex.TypeKind.FUNCTIONNOPROTO: "Function",
    cindex.TypeKind.FUNCTIONPROTO: "Function"
}

SYNTAX_GROUP = {
# Declarations
    cindex.CursorKind.UNEXPOSED_DECL: "cidx.unexposed_decl",
    cindex.CursorKind.STRUCT_DECL: "chromaticaStructDecl",
    cindex.CursorKind.UNION_DECL: "chromaticaUnionDecl",
    cindex.CursorKind.CLASS_DECL: "chromaticaClassDecl",
    cindex.CursorKind.ENUM_DECL: "chromaticaEnumDecl",
    cindex.CursorKind.FIELD_DECL: "chromaticaFieldDecl",
    cindex.CursorKind.ENUM_CONSTANT_DECL: "chromaticaEnumConstantDecl",
    cindex.CursorKind.FUNCTION_DECL: "chromaticaFunctionDecl",
    cindex.CursorKind.VAR_DECL: "chromaticaVarDecl",
    cindex.CursorKind.PARM_DECL: "chromaticaParmDecl",
    cindex.CursorKind.OBJC_INTERFACE_DECL: "chromaticaObjCInterfaceDecl",
    cindex.CursorKind.OBJC_CATEGORY_DECL: "chromaticaObjCCategoryDecl",
    cindex.CursorKind.OBJC_PROTOCOL_DECL: "chromaticaObjCProtocolDecl",
    cindex.CursorKind.OBJC_PROPERTY_DECL: "chromaticaObjCPropertyDecl",
    cindex.CursorKind.OBJC_IVAR_DECL: "chromaticaObjCIvarDecl",
    cindex.CursorKind.OBJC_INSTANCE_METHOD_DECL: "chromaticaObjCInstanceMethodDecl",
    cindex.CursorKind.OBJC_CLASS_METHOD_DECL: "chromaticaObjCClassMethodDecl",
    cindex.CursorKind.OBJC_IMPLEMENTATION_DECL: "chromaticaObjCImplementationDecl",
    cindex.CursorKind.OBJC_CATEGORY_IMPL_DECL: "chromaticaObjCCategoryImplDecl",
    cindex.CursorKind.TYPEDEF_DECL: "chromaticaTypedefDecl",
    cindex.CursorKind.CXX_METHOD: "chromaticaFunctionDecl",
    cindex.CursorKind.NAMESPACE: "chromaticaNamespace",
    cindex.CursorKind.LINKAGE_SPEC: "chromaticaLinkageSpec",
    cindex.CursorKind.CONSTRUCTOR: "chromaticaFunctionDecl",
    cindex.CursorKind.DESTRUCTOR: "chromaticaFunctionDecl",
    cindex.CursorKind.CONVERSION_FUNCTION: "chromaticaConversionFunction",
    cindex.CursorKind.TEMPLATE_TYPE_PARAMETER: "chromaticaTemplateTypeParameter",
    cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER: "chromaticaTemplateNoneTypeParameter",
    cindex.CursorKind.TEMPLATE_TEMPLATE_PARAMETER: "chromaticaTemplateTemplateParameter",
    cindex.CursorKind.FUNCTION_TEMPLATE: "chromaticaFunctionDecl",
    cindex.CursorKind.CLASS_TEMPLATE: "chromaticaClassDecl",
    cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION: "chromaticaClassTemplatePartialSpecialization",
    cindex.CursorKind.NAMESPACE_ALIAS: "chromaticaNamespaceAlias",
    cindex.CursorKind.USING_DIRECTIVE: "chromaticaUsingDirective",
    cindex.CursorKind.USING_DECLARATION: "chromaticaUsingDeclaration",
    cindex.CursorKind.TYPE_ALIAS_DECL: "chromaticaTypeAliasDecl",
    cindex.CursorKind.OBJC_SYNTHESIZE_DECL: "chromaticaObjCSynthesizeDecl",
    cindex.CursorKind.OBJC_DYNAMIC_DECL: "chromaticaObjCDynamicDecl",
    cindex.CursorKind.CXX_ACCESS_SPEC_DECL: "chromaticaCXXAccessSpecifier",
# References
    cindex.CursorKind.OBJC_SUPER_CLASS_REF: "chromaticaObjCSuperClassRef",
    cindex.CursorKind.OBJC_PROTOCOL_REF: "chromaticaObjCProtocolRef",
    cindex.CursorKind.OBJC_CLASS_REF: "chromaticaObjCClassRef",
    cindex.CursorKind.TYPE_REF: "chromaticaTypeRef",  # class ref
    cindex.CursorKind.CXX_BASE_SPECIFIER: "chromaticaCXXBaseSpecifier",
    cindex.CursorKind.TEMPLATE_REF: "chromaticaTemplateRef",  # template class ref
    cindex.CursorKind.NAMESPACE_REF: "chromaticaNamespaceRef",  # namespace ref
    cindex.CursorKind.MEMBER_REF: "chromaticaDeclRefExprCall",  # ex: designated initializer
    cindex.CursorKind.LABEL_REF: "chromaticaLableRef",
    cindex.CursorKind.OVERLOADED_DECL_REF: "chromaticaOverloadDeclRef",
    cindex.CursorKind.VARIABLE_REF: "chromaticaVariableRef",
# Errors
    cindex.CursorKind.INVALID_FILE: None,
    cindex.CursorKind.NO_DECL_FOUND: None,
    cindex.CursorKind.NOT_IMPLEMENTED: None,
    cindex.CursorKind.INVALID_CODE: None,
# Expressions
    cindex.CursorKind.UNEXPOSED_EXPR: "cidx.unexposed_expr",
    cindex.CursorKind.DECL_REF_EXPR: TYPE_GROUP,
    cindex.CursorKind.MEMBER_REF_EXPR:
    {
        cindex.TypeKind.UNEXPOSED: "chromaticaMemberRefExprCall",  # member function call
    },
    cindex.CursorKind.CALL_EXPR: "chromaticaCallExpr",
    cindex.CursorKind.OBJC_MESSAGE_EXPR: "chromaticaObjCMessageExpr",
    cindex.CursorKind.BLOCK_EXPR: "chromaticaBlockExpr",

    # literals moved
    cindex.CursorKind.PAREN_EXPR: "cidx.paren_expr",
    cindex.CursorKind.UNARY_OPERATOR: "cidx.unary_operator",
    cindex.CursorKind.ARRAY_SUBSCRIPT_EXPR: "cidx.array_subscript_expr",
    cindex.CursorKind.BINARY_OPERATOR: "cidx.binary_operator",
    cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR: "cidx.compound_assignment_operator",
    cindex.CursorKind.CONDITIONAL_OPERATOR: "cidx.conditional_operator",
    cindex.CursorKind.CSTYLE_CAST_EXPR: "cidx.cstyle_cast_expr",
    cindex.CursorKind.INIT_LIST_EXPR: "cidx.init_list_expr",
    cindex.CursorKind.ADDR_LABEL_EXPR: "cidx.addr_label_expr",
    cindex.CursorKind.StmtExpr: "cidx.stmt_expr",
    cindex.CursorKind.GENERIC_SELECTION_EXPR: "cidx.generic_selection_expr",
    cindex.CursorKind.GNU_NULL_EXPR: "cidx.gnu_null_expr",
    cindex.CursorKind.CXX_STATIC_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_DYNAMIC_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_REINTERPRET_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_CONST_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_FUNCTIONAL_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_TYPEID_EXPR: "cidx.cxx_typeid_expr",
    cindex.CursorKind.CXX_BOOL_LITERAL_EXPR: "chromaticaBoolean",
    cindex.CursorKind.CXX_NULL_PTR_LITERAL_EXPR: "chromaticaConstant",
    cindex.CursorKind.CXX_THIS_EXPR: "chromaticaStatement",

    cindex.CursorKind.CXX_THROW_EXPR: "chromaticaStatement",
    cindex.CursorKind.CXX_NEW_EXPR: "chromaticaStatement",
    cindex.CursorKind.CXX_DELETE_EXPR: "chromaticaStatement",
    cindex.CursorKind.CXX_UNARY_EXPR: "chromaticaStatement",
    cindex.CursorKind.OBJC_ENCODE_EXPR: "cidx.objc_encode_expr",
    cindex.CursorKind.OBJC_SELECTOR_EXPR: "cidx.objc_selector_expr",
    cindex.CursorKind.OBJC_PROTOCOL_EXPR: "cidx.objc_protocol_expr",
    cindex.CursorKind.OBJC_BRIDGE_CAST_EXPR: "cidx.objc_bridge_cast_expr",
    cindex.CursorKind.PACK_EXPANSION_EXPR: "cidx.pack_expansion_expr",
    cindex.CursorKind.SIZE_OF_PACK_EXPR: "cidx.size_of_pack__expr",
    cindex.CursorKind.LAMBDA_EXPR: "cidx.lambda_expr",
    cindex.CursorKind.OBJ_BOOL_LITERAL_EXPR: "cidx.obj_bool_literal_expr",
    cindex.CursorKind.OBJ_SELF_EXPR: "cidx.obj_self_expr",
    cindex.CursorKind.OMP_ARRAY_SECTION_EXPR: "cidx.omp_array_section_expr",

    cindex.CursorKind.UNEXPOSED_STMT: "cidx.unexposed_expr",
    cindex.CursorKind.LABEL_STMT: "chromaticaStatement",
    cindex.CursorKind.COMPOUND_STMT: "cidx.compound_expr",
    cindex.CursorKind.CASE_STMT: "chromaticaSwitch",
    cindex.CursorKind.DEFAULT_STMT: "chromaticaSwitch",
    cindex.CursorKind.IF_STMT: "chromaticaIf",
    cindex.CursorKind.SWITCH_STMT: "chromaticaSwitch",
    cindex.CursorKind.WHILE_STMT: "chromaticaLoop",
    cindex.CursorKind.DO_STMT: "chromaticaLoop",
    cindex.CursorKind.FOR_STMT: "chromaticaLoop",
    cindex.CursorKind.GOTO_STMT: "chromaticaStatement",
    cindex.CursorKind.INDIRECT_GOTO_STMT: "chromaticaStatement",
    cindex.CursorKind.CONTINUE_STMT: "chromaticaStatement",
    cindex.CursorKind.BREAK_STMT: "chromaticaStatement",
    cindex.CursorKind.RETURN_STMT: "chromaticaStatement",
    cindex.CursorKind.ASM_STMT: "chromaticaStatement",
    cindex.CursorKind.OBJC_AT_TRY_STMT: "cidx.objc_at_try_expr",
    cindex.CursorKind.OBJC_AT_CATCH_STMT: "cidx.objc_at_catch_expr",
    cindex.CursorKind.OBJC_AT_FINALLY_STMT: "cidx.objc_at_finally_expr",
    cindex.CursorKind.OBJC_AT_THROW_STMT: "cidx.objc_at_throw_expr",
    cindex.CursorKind.OBJC_AT_SYNCHRONIZED_STMT: "cidx.objc_at_synchronized_expr",
    cindex.CursorKind.OBJC_AUTORELEASE_POOL_STMT: "cidx.objc_autorelease_pool_expr",
    cindex.CursorKind.OBJC_FOR_COLLECTION_STMT: "cidx.objc_for_collection_expr",
    cindex.CursorKind.CXX_CATCH_STMT: "chromaticaExceptionStatement",
    cindex.CursorKind.CXX_TRY_STMT: "chromaticaExceptionStatement",
    cindex.CursorKind.CXX_FOR_RANGE_STMT: "chromaticaLoop",
    cindex.CursorKind.SEH_TRY_STMT: "chromaticaMSStatement",
    cindex.CursorKind.SEH_EXCEPT_STMT: "chromaticaMSStatement",
    cindex.CursorKind.SEH_FINALLY_STMT: "chromaticaMSStatement",
    cindex.CursorKind.MS_ASM_STMT: "chromaticaMSStatement",
    cindex.CursorKind.NULL_STMT: "cidx.NULL_expr",
    cindex.CursorKind.DECL_STMT: "cidx.DECL_expr",

    cindex.CursorKind.UNEXPOSED_ATTR: "cidx.unexposed_expr",
    cindex.CursorKind.IB_ACTION_ATTR: "cidx.ib_action_attr",
    cindex.CursorKind.IB_OUTLET_ATTR: "cidx.ib-action-attr",
    cindex.CursorKind.IB_OUTLET_COLLECTION_ATTR: "cidx.ib-outlet-collection-attr",
    cindex.CursorKind.CXX_FINAL_ATTR: "cidx.cxx-final-attr",
    cindex.CursorKind.CXX_OVERRIDE_ATTR: "cidx.cxx-override-attr",
    cindex.CursorKind.ANNOTATE_ATTR: "cidx.annotate-attr",
    cindex.CursorKind.ASM_LABEL_ATTR: "cidx.asm-label-attr",
    cindex.CursorKind.PACKED_ATTR: "cidx.packed-attr",
    cindex.CursorKind.PURE_ATTR: "cidx.pure-atte",
    cindex.CursorKind.CONST_ATTR: "cidx.const-attr",
    cindex.CursorKind.NODUPLICATE_ATTR: "cidx.noduplicatte-attr",
    cindex.CursorKind.CUDACONSTANT_ATTR: "cidx.cudaconstant-attr",
    cindex.CursorKind.CUDADEVICE_ATTR: "cidx.cudadevice-attr",
    cindex.CursorKind.CUDAGLOBAL_ATTR: "cidx.cudaglobal-attr",
    cindex.CursorKind.CUDAHOST_ATTR: "cidx.cudahost-attr",
    cindex.CursorKind.CUDASHARED_ATTR: "cidx.cudashared-attr",
    cindex.CursorKind.VISIBILITY_ATTR: "cidx.visibility-attr",
    cindex.CursorKind.DLLEXPORT_ATTR: "cidx.dllexport-attr",
    cindex.CursorKind.DLLIMPORT_ATTR: "cidx.dllimport-attr",

    cindex.CursorKind.PREPROCESSING_DIRECTIVE: "cidx.preprocessing_directive",
    cindex.CursorKind.MACRO_DEFINITION: "cidx.macro_definition",
    cindex.CursorKind.MACRO_INSTANTIATION: "chromaticaMacroInstantiation",
    cindex.CursorKind.INCLUSION_DIRECTIVE: "chromaticaInclusionDirective",
}

def _get_default_syn(cursor_kind):
    if cursor_kind.is_preprocessing():
        return "chromaticaPrepro"
    elif cursor_kind.is_declaration():
        return "chromaticaDecl"
    elif cursor_kind.is_reference():
        return "chromaticaRef"
    else:
        return "chromaticaDEFSYN"

def _get_keyword_syn(cursor_kind):
    """Handles cursor type of keyword tokens. Providing syntax group for most
    keywords"""
    if cursor_kind.is_statement():
        return SYNTAX_GROUP.get(cursor_kind)
    elif cursor_kind.is_declaration(): # hack for function return type and others
        return "chromaticaType"
    elif cursor_kind.is_attribute():
        return SYNTAX_GROUP.get(cursor_kind)
    elif cursor_kind.is_expression():
        return SYNTAX_GROUP.get(cursor_kind)
    else:
        return "chromaticaKeyword"

def _get_syntax_group(token, cursor):
    if token.kind.value == 1: # Keyword
        return _get_keyword_syn(cursor.kind)

    elif token.kind.value == 2: # Identifier
        group = _get_default_syn(cursor.kind)

        _group = SYNTAX_GROUP.get(cursor.kind)
        if _group:
            if cursor.kind == cindex.CursorKind.DECL_REF_EXPR:
                _group = custom.get(cursor.type.kind)
                if _group:
                    group = _group
            elif cursor.kind == cindex.CursorKind.MEMBER_REF_EXPR:
                _group = _group.get(cursor.type.kind)
                if _group:
                    group = _group
                else:
                    group = "chromaticaMemberRefExprVar"
            else:
                group = _group
        return group

    elif token.kind.value == 3: # Literal
        literal_type = LITERAL_GROUP.get(cursor.kind)
        if literal_type:
            return literal_type
        else:
            return "%s" % literal_type

    elif token.kind.value == 4: # Comment
        return "Comment"

    else: # Punctuation
        return None

def get_highlight(tu, filename, lbegin, lend):
    file = tu.get_file(filename)

    if not file:
        return None, None

    begin = cindex.SourceLocation.from_position(tu, file, line=lbegin, column=1)
    end   = cindex.SourceLocation.from_position(tu, file, line=lend+1, column=1)
    tokens = tu.get_tokens(extent=cindex.SourceRange.from_locations(begin, end))

    syntax = {}

    for token in tokens:
        cursor = token.cursor
        cursor._tu = tu

        pos = [token.location.line, token.location.column, len(token.spelling)]
        group = _get_syntax_group(token, cursor)

        if group:
            if group not in syntax:
                syntax[group] = []

            syntax[group].append(pos)

    return syntax

def get_highlight2(tu, filename, lbegin, lend):
    fp = open("AST_out.log", "w")
    file = tu.get_file(filename)

    if not file:
        return None

    begin = cindex.SourceLocation.from_position(tu, file, line=lbegin, column=1)
    end   = cindex.SourceLocation.from_position(tu, file, line=lend+1, column=1)
    tokens = tu.get_tokens(extent=cindex.SourceRange.from_locations(begin, end))

    syntax = {}
    output = {}

    for token in tokens:
        cursor = token.cursor
        cursor._tu = tu

        symbol = token.spelling
        pos = [token.location.line, token.location.column, len(token.spelling)]
        group = _get_syntax_group(token, cursor)

        if group:
            fp.write("%s %s %s %s\n" % (symbol, group, pos, cursor.kind))

    fp.close()

