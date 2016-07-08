
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
    cindex.CursorKind.STRING_LITERAL: None,
    cindex.CursorKind.CHARACTER_LITERAL: "Character",
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
    cindex.CursorKind.UNEXPOSED_DECL: None,
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
    cindex.CursorKind.UNEXPOSED_EXPR: None,
    cindex.CursorKind.DECL_REF_EXPR: TYPE_GROUP,
    cindex.CursorKind.MEMBER_REF_EXPR:
    {
        cindex.TypeKind.UNEXPOSED: "chromaticaMemberRefExprCall",  # member function call
    },
    cindex.CursorKind.CALL_EXPR: "chromaticaCallExprt",
    cindex.CursorKind.OBJC_MESSAGE_EXPR: "chromaticaObjCMessageExpr",
    cindex.CursorKind.BLOCK_EXPR: "chromaticaBlockExpr",
    cindex.CursorKind.MACRO_INSTANTIATION: "chromaticaMacroInstantiation",
    cindex.CursorKind.INCLUSION_DIRECTIVE: "chromaticaInclusionDirective",
    cindex.CursorKind.COMPOUND_STMT: None,
    cindex.CursorKind.PAREN_EXPR: None,
    cindex.CursorKind.CXX_FOR_RANGE_STMT: None,
    cindex.CursorKind.DECL_STMT: None,

}

def _get_default_syn(cursor_kind):
    if cursor_kind.is_preprocessing():
        return "chromaticaPrepro"
    elif cursor_kind.is_declaration():
        return "chromaticaDecl"
    elif cursor_kind.is_reference():
        return "chromaticaRef"
    else:
        return None


def _get_syntax_group(token, cursor):
    if token.kind.value == 3:
        literal_type = LITERAL_GROUP.get(cursor.kind)
        if literal_type:
            return literal_type
        else:
            return None

    elif token.kind.value == 2:
        group = _get_default_syn(cursor.kind)

        custom = SYNTAX_GROUP.get(cursor.kind)
        if custom:
            if cursor.kind == cindex.CursorKind.DECL_REF_EXPR:
                custom = custom.get(cursor.type.kind)
                if custom:
                    group = custom
            elif cursor.kind == cindex.CursorKind.MEMBER_REF_EXPR:
                custom = custom.get(cursor.type.kind)
                if custom:
                    group = custom
                else:
                    group = "chromaticaMemberRefExprVar"
            else:
                group = custom

        return group
    else:
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

