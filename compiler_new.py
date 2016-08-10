# -------------------------------------------------------------------------------
# Project:     mysite
# Name:        compiler
# Purpose:     
# Author:      zWX206936
# Created:     2016/8/5 9:33
# Copyright:   (c) "zWX206936" "2016/8/5 9:33" 
# Licence:     <your licence>
# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------------
"""

"""

"""
/**
* ������������дһ����������һ�������޵�С�ı���������С�����������ע��ɾȥ�Ļ������ֻʣ
* 200�����ҵĴ��롣
* 
* ���ǽ��������� lisp ���ĺ�������ת��Ϊ C ���
*
* �����������ַ���Ǻ���Ϥ��������һ���򵥵Ľ��ܡ�
*
* ��������������������`add` �� `subtract`����ô���ǵ�д������������������
* 
*                  LISP                      C
*
*   2 + 2          (add 2 2)                 add(2, 2)
*   4 - 2          (subtract 4 2)            subtract(4, 2)
*   2 + (4 - 2)    (add 2 (subtract 4 2))    add(2, subtract(4, 2))
*
* �ܼ򵥶԰ɣ�
*
* ���ת���������ǽ�Ҫ�������顣��Ȼ�Ⲣ������ LISP ���� C ��ȫ���﷨����������������
* չʾ�ִ��������ܶ�Ҫ�㡣
* 
*/

/**
* ��������������Էֳ������׶Σ�������Parsing����ת����Transformation���Լ�����
* ���ɣ�Code Generation��
*
* 1.*����*�ǽ����ԭʼ�Ĵ���ת��Ϊһ�ָ��ӳ���ı�ʾ������ע����AST����*
*
* 2.*ת��*�����������ı�ʾ��һЩ������������������������
*    �����������顣
*
* 3.*��������*���մ���֮��Ĵ����ʾ��Ȼ�����ת�����µĴ��롣
*/
"""
'''
/**
* ������Parsing��
* -------
*
* ����һ����˵��ֳ������׶Σ��ʷ�������Lexical Analysis�����﷨������Syntactic Analysis����
*
* 1.*�ʷ�����*����ԭʼ���룬Ȼ������ָ��һЩ����Ϊ Token �Ķ���������������ڴʷ�����
*    ����Tokenizer����Lexer������ɵġ�
*
*    Token ��һ�����飬��һЩ����������Ƭ��ɡ����ǿ��������֡���ǩ�������š��������
*    ���������κζ�����
*
* 2.*�﷨����* ����֮ǰ���ɵ� Token��������ת����һ�ֳ���ı�ʾ�����ֳ���ı�ʾ�����˴�
*    ������е�ÿһ��Ƭ���Լ�����֮��Ĺ�ϵ���ⱻ��Ϊ�м��ʾ��intermediate representation��
*    ������﷨����Abstract Syntax Tree�� ��дΪAST��
*
*    �����﷨����һ��Ƕ�׳̶Ⱥ���Ķ�����һ�ָ����״���ķ�ʽ�����˴��뱾��Ҳ�ܸ�����
*    ������Ϣ��
*
* ����˵����������һ�д�����䣺
*
*   (add 2 (subtract 4 2))
*
* �������� Token �����������������ģ�
*
*   [
*     { type: 'paren',  value: '('        },
*     { type: 'name',   value: 'add'      },
*     { type: 'number', value: '2'        },
*     { type: 'paren',  value: '('        },
*     { type: 'name',   value: 'subtract' },
*     { type: 'number', value: '4'        },
*     { type: 'number', value: '2'        },
*     { type: 'paren',  value: ')'        },
*     { type: 'paren',  value: ')'        }
*   ]
*
* ���ĳ����﷨����AST�������������������ģ�
*
*   {
*     type: 'Program',
*     body: [{
*       type: 'CallExpression',
*       name: 'add',
*       params: [{
*         type: 'NumberLiteral',
*         value: '2'
*       }, {
*         type: 'CallExpression',
*         name: 'subtract',
*         params: [{
*           type: 'NumberLiteral',
*           value: '4'
*         }, {
*           type: 'NumberLiteral',
*           value: '2'
*         }]
*       }]
*     }]
*   }
*/

/**
* ת����Transformation��
* --------------
*
* ����������һ������ת������ֻ�ǰ� AST �ù���Ȼ�������һЩ�޸ġ���������ͬ�������²�
* �� AST��Ҳ���԰� AST �����ȫ�µ����ԡ�
*
* �������������������ת�� AST��
*
* �����ע�⵽�����ǵ� AST ���кܶ����Ƶ�Ԫ�أ���ЩԪ�ض��� type ���ԣ����Ǳ���Ϊ AST
* ��㡣��Щ��㺬���������ԣ������������� AST �Ĳ�����Ϣ��
*
* ����������һ����NumberLiteral����㣺
*
*   {
*     type: 'NumberLiteral',
*     value: '2'
*   }
*
* �ֱ���������һ����CallExpression����㣺
*
*   {
*     type: 'CallExpression',
*     name: 'subtract',
*     params: [...nested nodes go here...]
*   }
*
* ��ת�� AST ��ʱ�����ǿ�����ӡ��ƶ��������Щ��㣬Ҳ���Ը������е� AST ����һ��ȫ��
* �� AST
*
* ��Ȼ���Ǳ�������Ŀ���ǰ�����Ĵ���ת��Ϊһ���µ����ԣ��������ǽ��������ڲ���һ�����
* �����Ե�ȫ�µ� AST��
* 
*
* ������Traversal��
* ---------
*
* Ϊ���ܴ������еĽ�㣬������Ҫ�������ǣ�ʹ�õ���������ȱ�����
*
*   {
*     type: 'Program',
*     body: [{
*       type: 'CallExpression',
*       name: 'add',
*       params: [{
*         type: 'NumberLiteral',
*         value: '2'
*       }, {
*         type: 'CallExpression',
*         name: 'subtract',
*         params: [{
*           type: 'NumberLiteral',
*           value: '4'
*         }, {
*           type: 'NumberLiteral',
*           value: '2'
*         }]
*       }]
*     }]
*   }
*
* So for the above AST we would go:
* ��������� AST �ı��������������ģ�
*
*   1. Program - �� AST �Ķ�����㿪ʼ
*   2. CallExpression (add) - Program �ĵ�һ����Ԫ��
*   3. NumberLiteral (2) - CallExpression (add) �ĵ�һ����Ԫ��
*   4. CallExpression (subtract) - CallExpression (add) �ĵڶ�����Ԫ��
*   5. NumberLiteral (4) - CallExpression (subtract) �ĵ�һ����Ԫ��
*   6. NumberLiteral (4) - CallExpression (subtract) �ĵڶ�����Ԫ��
*
* �������ֱ���� AST �ڲ������������ǲ���һ���µ� AST����ô��Ҫ�����������������ĳ���
* ����Ŀǰ���ʣ�visiting�����н��ķ����Ѿ��㹻�ˡ�
*
* ʹ�á����ʣ�visiting��������ʵ�����Ϊ����һ��ģʽ�������ڶ���ṹ�ڶ�Ԫ�ؽ��в�����
*
* �����ߣ�Visitors��
* --------
*
* ������������뷨�Ǵ���һ���������ߣ�visitor����������������а���һЩ���������Խ��ղ�
* ͬ�Ľ�㡣
*
*   var visitor = {
*     NumberLiteral() {},
*     CallExpression() {}
*   };
*
* �����Ǳ��� AST ��ʱ�����������ƥ�� type �Ľ�㣬���ǿ��Ե��� visitor �еķ�����
*
* һ�������Ϊ������Щ���������Ը��ã����ǻ�Ѹ����Ҳ��Ϊ�������롣
*/

/**
* �������ɣ�Code Generation��
* ---------------
*
* �����������һ���׶��Ǵ������ɣ�����׶�����������ʱ����ת����transformation���ص���
* ���Ǵ�����������Ҫ�Ĳ��ֻ��Ǹ��� AST ��������롣
*
* ���������м��ֲ�ͬ�Ĺ�����ʽ����Щ��������������֮ǰ���ɵ� token����Щ�ᴴ�������Ĵ���
* ��ʾ���Ա������Ե�������롣���ǽ��������ǻ���������ʹ��֮ǰ���ɺõ� AST��
*
* ���ǵĴ�����������Ҫ֪����Ρ���ӡ��AST ���������͵Ľ�㣬Ȼ������ݹ�ص�������ֱ����
* �д��붼����ӡ��һ���ܳ����ַ����С�
* 
*/

/**
* ���ˣ�����Ǳ����������еĲ����ˡ�
*
* ��Ȼ����˵���еı�����������˵����������ͬ�ı������в�ͬ��Ŀ�ģ�����Ҳ������Ҫ��ͬ�Ĳ��衣
*
* ��������Ӧ�öԱ����������Ǹ�ʲô�����и���ŵ���ʶ�ˡ�
*
* ��Ȼ��ȫ������һ���ˣ���Ӧ����дһ�������Լ��ı������˰ɣ�
*
* ����������Ц�������������ص� :P
*
* �������ǿ�ʼ��...
*/
'''
'''
/**
* =======================================================================
*                              (/^��^)/
*                       �ʷ���������Tokenizer��!
* =======================================================================
*/

/**
* ���Ǵӵ�һ���׶ο�ʼ�����ʷ�������ʹ�õ��Ǵʷ���������Tokenizer����
*
* ����ֻ�ǽ��մ�����ɵ��ַ�����Ȼ������Ƿָ�� token ��ɵ����顣
*
*   (add 2 (subtract 4 2))   =>   [{ type: 'paren', value: '(' }, ...]
*/
'''


def tokenizer(string):
    # current ������¼��ǰ���봮��λ��
    current = 0
    # tokens ����token
    tokens = []
    # ����whileѭ����current������ѭ��������
    while (current < len(string)):
        char = string[current]
        # ����ǲ���������
        if (char == '('):
            # ����������ţ�����뵽tokens
            tokens.append({"type": "paren", "value": "("})
            current += 1
            continue
        # ����ǲ���������
        if (char == ')'):
            tokens.append({"type": "paren", "value": ")"})
            current += 1
            continue
        # ����ǿո�������
        if (char.isspace()):
            current += 1
            continue
        # ����Ƿ�������
        if (char.isdigit()):
            value = ''
            # �������������
            while (char.isdigit()):
                value += char
                current += 1
                char = string[current]
            tokens.append({"type": "number", "value": value})
            continue
        # ����Ƿ���ĸ���������token����Ϊname
        if (char.isalpha()):
            value = ''
            while (char.isalpha()):
                value += char
                current += 1
                char = string[current]
            tokens.append({"type": "name", "value": value})
            continue
    return tokens


"""
/**
* =======================================================================
*                            �c/?o  ? o\?
*                        �﷨��������Parser��!!!
* =======================================================================
*/

/**
*  �﷨���������� token ���飬Ȼ�����ת��Ϊ AST
*
*   [{ type: 'paren', value: '(' }, ...]   =>   { type: 'Program', body: [...] }
*/

"""


def parser(tokens):
    tokens = tokens
    curr = 0
    def walk(curr):
        token = tokens[curr]
        if (token['type'] == 'number'):
            curr += 1
            return curr,{'type': 'NumberLiteral', 'value': token['value']}
        if (token['type'] == 'paren' and token['value'] == '('):
            curr += 1
            token = tokens[curr]
            node = {'type': 'CallExpression', 'name': token['value'], 'params': []}
            curr += 1
            token = tokens[curr]
            while (not (token['type'] == 'paren' and token['value'] == ')')):
                curr, params = walk(curr)
                node['params'].append(params)
                token = tokens[curr]
            curr += 1
            return curr, node
    ast = {'type': 'Program', 'body': []}
    while (curr < len(tokens)):
        curr, node = walk(curr)
        ast['body'].append(node)
    return ast


'''
/**
 * ������������ AST��������Ҫһ�� visitor ȥ�������еĽ�㡣������ĳ�����͵Ľ��ʱ������
 * ��Ҫ���� visitor �ж�Ӧ���͵Ĵ�������
 *
 *   traverse(ast, {
 *     Program(node, parent) {
 *       // ...
 *     },
 *
 *     CallExpression(node, parent) {
 *       // ...
 *     },
 *
 *     NumberLiteral(node, parent) {
 *       // ...
 *     }
 *   });
 */
'''
def traverser(ast, visitor):
    def traverseNode(node, parent):
        method = visitor[node['type']]
        print(method, hasattr(method, '__call__'))
        if (hasattr(method, '__call__')) :
            method(node, parent)
        if(node['type'] == 'Program'):
            traverseArray(node['body'], node)
        elif(node['type'] == 'CallExpression'):
            traverseArray(node['params'], node)
        elif(node['type'] == 'NumberLiteral'):
            pass
        else:
            pass

    def traverseArray(array, parent):
        for child, parent in array:
            lambda child:traverseNode(child, parent)
    traverseNode(ast, None)

'''
/**
 * ������ת������ת��������������֮ǰ�����õ� AST��Ȼ������� visitor ���ݽ������ǵı���
 * ���� �����õ�һ���µ� AST��
 *
 * ----------------------------------------------------------------------------
 *            ԭʼ�� AST               |               ת����� AST
 * ----------------------------------------------------------------------------
 *   {                                |   {
 *     type: 'Program',               |     type: 'Program',
 *     body: [{                       |     body: [{
 *       type: 'CallExpression',      |       type: 'ExpressionStatement',
 *       name: 'add',                 |       expression: {
 *       params: [{                   |         type: 'CallExpression',
 *         type: 'NumberLiteral',     |         callee: {
 *         value: '2'                 |           type: 'Identifier',
 *       }, {                         |           name: 'add'
 *         type: 'CallExpression',    |         },
 *         name: 'subtract',          |         arguments: [{
 *         params: [{                 |           type: 'NumberLiteral',
 *           type: 'NumberLiteral',   |           value: '2'
 *           value: '4'               |         }, {
 *         }, {                       |           type: 'CallExpression',
 *           type: 'NumberLiteral',   |           callee: {
 *           value: '2'               |             type: 'Identifier',
 *         }]                         |             name: 'subtract'
 *       }]                           |           },
 *     }]                             |           arguments: [{
 *   }                                |             type: 'NumberLiteral',
 *                                    |             value: '4'
 * ---------------------------------- |           }, {
 *                                    |             type: 'NumberLiteral',
 *                                    |             value: '2'
 *                                    |           }]
 *         (��һ�߱Ƚϳ�/w\)            |         }]
 *                                    |       }
 *                                    |     }]
 *                                    |   }
 * ----------------------------------------------------------------------------
 */
'''

#�������, ���get('body')��ȡ���Ĳ���һ��list��˵��û���ӽڵ�, ĳ���ڵ��visit���Բ�ΪNone��˵���ýڵ㼰���ӽڵ��ѱ�����
#{'body': [{'params': [{'value': '2', 'type': 'NumberLiteral'}, {'params': [{'value': '4', 'type': 'NumberLiteral'},
# {'value': '2', 'type': 'NumberLiteral'}], 'type': 'CallExpression', 'name': 'subtract'}], 'type': 'CallExpression', 'name': 'add'}], 'type': 'Program'}
astlist = []
def transformer(ast):
    if(ast.get('type') == 'Program'):
        astlist.append(ast)
        if(ast.get('visit') == None):
            ast['visit'] = {'type': 'Pragrom', 'body':[]}
            for node in ast.get('body'):
                transformer(node)
        else:
            for node in ast.get('body'):
                appnode = node['visit'].copy()
                ast['visit']['body'].append(appnode)
    if(ast.get('type') == 'CallExpression'):
        if (ast.get('visit') == None):
            ast['visit'] = {'type':'CallExpression','callee':{'type':'Identifier', 'name':ast['name']}, 'arguments':[]}
            astlist.append(ast)
            for node in ast.get('params'):
                astlist.append(node)
            transformer(astlist.pop())
        else:
            for node in ast.get('params'):
                appnode = node['visit'].copy()
                ast['visit']['arguments'].append(appnode)
            ast = astlist.pop()
            transformer(ast)
    if(ast.get('type') == 'NumberLiteral' and ast.get('visit') == None):
        ast['visit'] = {'type': 'NumberLiteral', 'value': ast['value']}
        ast = astlist.pop()
        transformer(ast)

def transform(ast):
    transformer(ast)
    ast = ast.get('visit')
    return ast






'''
/**
 * =======================================================================
 *                          �d������?�ޣ�??
 *                           ����������!!!!
 * =======================================================================
 */

/**
 * ����ֻʣ���һ������������������
 *
 * ���ǵĴ�����������ݹ�ص������Լ����� AST �е�ÿ������ӡ��һ���ܴ���ַ����С�
 */
'''
def codeGenerator(node):
    pass
