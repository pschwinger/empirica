#!/usr/bin/env python3
"""
🔍 Functionality Analyzer Component
Self-contained code analysis and semantic understanding for AI systems

This component provides comprehensive code analysis capabilities including:
- Basic code structure analysis and understanding
- Semantic pattern recognition and classification
- Function and class signature analysis
- Code quality and complexity assessment
"""

from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import re
import ast
import inspect
from datetime import datetime

# ============================================================================
# CORE CODE ANALYZER (from original ai_archaeologist.py)
# ============================================================================

class CodeElementType(Enum):
    """Types of code elements"""
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    VARIABLE = "variable"
    CONSTANT = "constant"
    IMPORT = "import"
    DECORATOR = "decorator"

@dataclass
class FunctionSignature:
    """Represents a function signature"""
    name: str
    parameters: List[str]
    return_type: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    line_number: int = 0
    is_async: bool = False
    is_private: bool = False
    is_magic: bool = False

@dataclass
class CodeComponent:
    """Represents a code component"""
    name: str
    element_type: CodeElementType
    location: Tuple[int, int]  # (start_line, end_line)
    signature: Optional[FunctionSignature] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    complexity_score: float = 0.0
    dependencies: List[str] = field(default_factory=list)

class CodeAnalyzer:
    """
    Basic code analysis and archaeological investigation
    Provides foundational code understanding capabilities
    """
    
    def __init__(self):
        self.components: List[CodeComponent] = []
        self.analysis_results: Dict[str, Any] = {}
        self.file_metrics: Dict[str, Any] = {}
        
    def analyze_file(self, file_path: str, content: str = None) -> Dict[str, Any]:
        """Analyze a Python file for structure and components"""
        try:
            if content is None:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            # Parse AST for accurate analysis
            tree = ast.parse(content)
            
            # Reset analysis state
            self.components = []
            
            # Analyze AST nodes
            self._analyze_ast(tree, content.split('\n'))
            
            # Calculate file metrics
            self.file_metrics = self._calculate_file_metrics(content, file_path)
            
            # Compile analysis results
            self.analysis_results = {
                'file_path': file_path,
                'components': self.components,
                'metrics': self.file_metrics,
                'analyzed_at': datetime.now().isoformat()
            }
            
            return self.analysis_results
            
        except Exception as e:
            print(f"❌ Error analyzing file {file_path}: {e}")
            return {'error': str(e), 'file_path': file_path}
    
    def _analyze_ast(self, tree: ast.AST, lines: List[str]):
        """Analyze AST nodes to extract code components"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._analyze_function(node, lines)
            elif isinstance(node, ast.AsyncFunctionDef):
                self._analyze_function(node, lines, is_async=True)
            elif isinstance(node, ast.ClassDef):
                self._analyze_class(node, lines)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self._analyze_import(node, lines)
            elif isinstance(node, ast.Assign):
                self._analyze_assignment(node, lines)
    
    def _analyze_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], 
                         lines: List[str], is_async: bool = False):
        """Analyze function definition"""
        try:
            # Extract function signature
            signature = FunctionSignature(
                name=node.name,
                parameters=[arg.arg for arg in node.args.args],
                return_type=self._get_return_annotation(node),
                decorators=[self._get_decorator_name(dec) for dec in node.decorator_list],
                docstring=ast.get_docstring(node),
                line_number=node.lineno,
                is_async=is_async,
                is_private=node.name.startswith('_'),
                is_magic=node.name.startswith('__') and node.name.endswith('__')
            )
            
            # Calculate complexity
            complexity = self._calculate_complexity(node)
            
            # Create component
            component = CodeComponent(
                name=node.name,
                element_type=CodeElementType.FUNCTION,
                location=(node.lineno, getattr(node, 'end_lineno', node.lineno)),
                signature=signature,
                complexity_score=complexity,
                attributes={
                    'parameter_count': len(signature.parameters),
                    'has_docstring': signature.docstring is not None,
                    'decorator_count': len(signature.decorators)
                }
            )
            
            self.components.append(component)
            
        except Exception as e:
            print(f"Error analyzing function {getattr(node, 'name', 'unknown')}: {e}")
    
    def _analyze_class(self, node: ast.ClassDef, lines: List[str]):
        """Analyze class definition"""
        try:
            # Extract class information
            base_classes = [self._get_name(base) for base in node.bases]
            methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            
            component = CodeComponent(
                name=node.name,
                element_type=CodeElementType.CLASS,
                location=(node.lineno, getattr(node, 'end_lineno', node.lineno)),
                attributes={
                    'base_classes': base_classes,
                    'method_count': len(methods),
                    'has_docstring': ast.get_docstring(node) is not None,
                    'is_private': node.name.startswith('_'),
                    'decorators': [self._get_decorator_name(dec) for dec in node.decorator_list]
                }
            )
            
            self.components.append(component)
            
        except Exception as e:
            print(f"Error analyzing class {getattr(node, 'name', 'unknown')}: {e}")
    
    def _analyze_import(self, node: Union[ast.Import, ast.ImportFrom], lines: List[str]):
        """Analyze import statement"""
        try:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    component = CodeComponent(
                        name=alias.name,
                        element_type=CodeElementType.IMPORT,
                        location=(node.lineno, node.lineno),
                        attributes={
                            'import_type': 'direct',
                            'alias': alias.asname
                        }
                    )
                    self.components.append(component)
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    component = CodeComponent(
                        name=f"{module}.{alias.name}",
                        element_type=CodeElementType.IMPORT,
                        location=(node.lineno, node.lineno),
                        attributes={
                            'import_type': 'from',
                            'module': module,
                            'name': alias.name,
                            'alias': alias.asname
                        }
                    )
                    self.components.append(component)
                    
        except Exception as e:
            print(f"Error analyzing import: {e}")
    
    def _analyze_assignment(self, node: ast.Assign, lines: List[str]):
        """Analyze variable assignment"""
        try:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    element_type = CodeElementType.CONSTANT if target.id.isupper() else CodeElementType.VARIABLE
                    
                    component = CodeComponent(
                        name=target.id,
                        element_type=element_type,
                        location=(node.lineno, node.lineno),
                        attributes={
                            'is_private': target.id.startswith('_'),
                            'is_constant': target.id.isupper(),
                            'value_type': type(node.value).__name__
                        }
                    )
                    self.components.append(component)
                    
        except Exception as e:
            print(f"Error analyzing assignment: {e}")
    
    def _calculate_complexity(self, node: ast.AST) -> float:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
                
        return float(complexity)
    
    def _calculate_file_metrics(self, content: str, file_path: str) -> Dict[str, Any]:
        """Calculate file-level metrics"""
        lines = content.split('\n')
        
        metrics = {
            'total_lines': len(lines),
            'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'function_count': len([c for c in self.components if c.element_type == CodeElementType.FUNCTION]),
            'class_count': len([c for c in self.components if c.element_type == CodeElementType.CLASS]),
            'import_count': len([c for c in self.components if c.element_type == CodeElementType.IMPORT]),
            'average_complexity': self._calculate_average_complexity(),
            'file_size': len(content)
        }
        
        return metrics
    
    def _calculate_average_complexity(self) -> float:
        """Calculate average complexity across functions"""
        function_complexities = [c.complexity_score for c in self.components 
                               if c.element_type == CodeElementType.FUNCTION and c.complexity_score > 0]
        
        if function_complexities:
            return sum(function_complexities) / len(function_complexities)
        return 0.0
    
    def _get_return_annotation(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Optional[str]:
        """Extract return type annotation"""
        if node.returns:
            return self._get_name(node.returns)
        return None
    
    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name"""
        return self._get_name(decorator)
    
    def _get_name(self, node: ast.expr) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        else:
            return str(type(node).__name__)
    
    def get_functions(self) -> List[CodeComponent]:
        """Get all function components"""
        return [c for c in self.components if c.element_type == CodeElementType.FUNCTION]
    
    def get_classes(self) -> List[CodeComponent]:
        """Get all class components"""
        return [c for c in self.components if c.element_type == CodeElementType.CLASS]
    
    def get_imports(self) -> List[CodeComponent]:
        """Get all import components"""
        return [c for c in self.components if c.element_type == CodeElementType.IMPORT]
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get comprehensive analysis summary"""
        return {
            'file_metrics': self.file_metrics,
            'component_counts': {
                'functions': len(self.get_functions()),
                'classes': len(self.get_classes()),
                'imports': len(self.get_imports()),
                'total': len(self.components)
            },
            'complexity_analysis': {
                'average_complexity': self._calculate_average_complexity(),
                'high_complexity_functions': [
                    c.name for c in self.get_functions() if c.complexity_score > 10
                ]
            },
            'code_quality_indicators': {
                'documented_functions': len([c for c in self.get_functions() 
                                           if c.signature and c.signature.docstring]),
                'private_functions': len([c for c in self.get_functions() 
                                        if c.signature and c.signature.is_private]),
                'magic_methods': len([c for c in self.get_functions() 
                                    if c.signature and c.signature.is_magic])
            }
        }

# ============================================================================
# SEMANTIC PATTERN ANALYSIS
# ============================================================================

class SemanticPatternType(Enum):
    """Types of semantic patterns"""
    FUNCTION_DEFINITION = "function_definition"
    CLASS_DEFINITION = "class_definition"
    VARIABLE_ASSIGNMENT = "variable_assignment"
    IMPORT_STATEMENT = "import_statement"
    CONTROL_FLOW = "control_flow"
    DATA_STRUCTURE = "data_structure"
    ALGORITHM_PATTERN = "algorithm_pattern"
    DESIGN_PATTERN = "design_pattern"

@dataclass
class SemanticPattern:
    """Represents a semantic pattern in code"""
    pattern_type: SemanticPatternType
    name: str
    location: Tuple[int, int]  # (line_start, line_end)
    confidence: float
    attributes: Dict[str, Any]
    description: str = ""

class SemanticAnalyzer:
    """
    Advanced semantic analysis for code understanding
    Provides pattern recognition and semantic interpretation
    """
    
    def __init__(self):
        self.patterns: List[SemanticPattern] = []
        self.semantic_rules: Dict[str, Any] = self._load_default_rules()
        self.code_analyzer = CodeAnalyzer()
        
    def analyze_code_semantics(self, code: str, file_path: str = "") -> List[SemanticPattern]:
        """Analyze code for semantic patterns"""
        self.patterns = []
        
        # First do basic code analysis
        analysis_results = self.code_analyzer.analyze_file(file_path, code)
        
        # Then extract semantic patterns
        self._extract_semantic_patterns(analysis_results)
        
        # Analyze design patterns
        self._analyze_design_patterns(analysis_results)
        
        return self.patterns
    
    def _extract_semantic_patterns(self, analysis_results: Dict[str, Any]):
        """Extract semantic patterns from code analysis"""
        components = analysis_results.get('components', [])
        
        for component in components:
            pattern = self._component_to_pattern(component)
            if pattern:
                self.patterns.append(pattern)
    
    def _component_to_pattern(self, component: CodeComponent) -> Optional[SemanticPattern]:
        """Convert code component to semantic pattern"""
        try:
            if component.element_type == CodeElementType.FUNCTION:
                return SemanticPattern(
                    pattern_type=SemanticPatternType.FUNCTION_DEFINITION,
                    name=component.name,
                    location=component.location,
                    confidence=0.9,
                    attributes={
                        'complexity': component.complexity_score,
                        'parameters': component.signature.parameters if component.signature else [],
                        'is_private': component.signature.is_private if component.signature else False,
                        'is_async': component.signature.is_async if component.signature else False
                    },
                    description=f"Function: {component.name}"
                )
            
            elif component.element_type == CodeElementType.CLASS:
                return SemanticPattern(
                    pattern_type=SemanticPatternType.CLASS_DEFINITION,
                    name=component.name,
                    location=component.location,
                    confidence=0.95,
                    attributes=component.attributes,
                    description=f"Class: {component.name}"
                )
            
            elif component.element_type == CodeElementType.IMPORT:
                return SemanticPattern(
                    pattern_type=SemanticPatternType.IMPORT_STATEMENT,
                    name=component.name,
                    location=component.location,
                    confidence=0.8,
                    attributes=component.attributes,
                    description=f"Import: {component.name}"
                )
                
        except Exception as e:
            print(f"Error converting component to pattern: {e}")
        
        return None
    
    def _analyze_design_patterns(self, analysis_results: Dict[str, Any]):
        """Analyze for common design patterns"""
        components = analysis_results.get('components', [])
        classes = [c for c in components if c.element_type == CodeElementType.CLASS]
        
        # Singleton pattern detection
        for cls in classes:
            if self._is_singleton_pattern(cls):
                pattern = SemanticPattern(
                    pattern_type=SemanticPatternType.DESIGN_PATTERN,
                    name=f"{cls.name}_singleton",
                    location=cls.location,
                    confidence=0.8,
                    attributes={'pattern': 'singleton', 'class': cls.name},
                    description=f"Singleton pattern in class {cls.name}"
                )
                self.patterns.append(pattern)
        
        # Factory pattern detection
        functions = [c for c in components if c.element_type == CodeElementType.FUNCTION]
        for func in functions:
            if self._is_factory_pattern(func):
                pattern = SemanticPattern(
                    pattern_type=SemanticPatternType.DESIGN_PATTERN,
                    name=f"{func.name}_factory",
                    location=func.location,
                    confidence=0.7,
                    attributes={'pattern': 'factory', 'function': func.name},
                    description=f"Factory pattern in function {func.name}"
                )
                self.patterns.append(pattern)
    
    def _is_singleton_pattern(self, cls: CodeComponent) -> bool:
        """Detect singleton pattern in class"""
        # Simple heuristic: class with private constructor or instance variable
        attributes = cls.attributes
        return (attributes.get('is_private', False) or 
                'instance' in str(attributes).lower() or
                '_instance' in cls.name.lower())
    
    def _is_factory_pattern(self, func: CodeComponent) -> bool:
        """Detect factory pattern in function"""
        # Simple heuristic: function name contains 'create', 'make', or 'factory'
        name_lower = func.name.lower()
        return any(keyword in name_lower for keyword in ['create', 'make', 'factory', 'build'])
    
    def _load_default_rules(self) -> Dict[str, Any]:
        """Load default semantic analysis rules"""
        return {
            'naming_conventions': {
                'function': 'snake_case',
                'class': 'PascalCase',
                'constant': 'UPPER_CASE',
                'private': 'starts_with_underscore'
            },
            'pattern_weights': {
                'function_definition': 1.0,
                'class_definition': 1.2,
                'import_statement': 0.8,
                'design_pattern': 1.5
            },
            'complexity_thresholds': {
                'low': 5,
                'medium': 10,
                'high': 20
            }
        }
    
    def get_semantic_summary(self) -> Dict[str, Any]:
        """Get summary of semantic analysis"""
        summary = {
            'total_patterns': len(self.patterns),
            'pattern_types': {},
            'confidence_avg': 0.0,
            'design_patterns': [],
            'complexity_distribution': {'low': 0, 'medium': 0, 'high': 0},
            'code_quality_score': 0.0
        }
        
        total_confidence = 0.0
        for pattern in self.patterns:
            pattern_type = pattern.pattern_type.value
            summary['pattern_types'][pattern_type] = summary['pattern_types'].get(pattern_type, 0) + 1
            total_confidence += pattern.confidence
            
            if pattern.pattern_type == SemanticPatternType.DESIGN_PATTERN:
                summary['design_patterns'].append(pattern.attributes.get('pattern', 'unknown'))
            
            # Analyze complexity
            complexity = pattern.attributes.get('complexity', 0)
            if complexity < 5:
                summary['complexity_distribution']['low'] += 1
            elif complexity < 10:
                summary['complexity_distribution']['medium'] += 1
            else:
                summary['complexity_distribution']['high'] += 1
        
        if self.patterns:
            summary['confidence_avg'] = total_confidence / len(self.patterns)
        
        # Calculate code quality score
        summary['code_quality_score'] = self._calculate_quality_score()
        
        return summary
    
    def _calculate_quality_score(self) -> float:
        """Calculate overall code quality score"""
        if not self.patterns:
            return 0.0
        
        # Factors: documentation, complexity, design patterns, naming conventions
        score = 0.0
        total_weight = 0.0
        
        # Documentation score
        documented_functions = len([p for p in self.patterns 
                                  if p.pattern_type == SemanticPatternType.FUNCTION_DEFINITION 
                                  and p.attributes.get('has_docstring', False)])
        total_functions = len([p for p in self.patterns 
                             if p.pattern_type == SemanticPatternType.FUNCTION_DEFINITION])
        
        if total_functions > 0:
            doc_score = documented_functions / total_functions
            score += doc_score * 0.3
            total_weight += 0.3
        
        # Complexity score (lower complexity is better)
        avg_complexity = sum(p.attributes.get('complexity', 0) for p in self.patterns) / len(self.patterns)
        complexity_score = max(0, 1 - (avg_complexity / 20))  # Normalize to 0-1
        score += complexity_score * 0.4
        total_weight += 0.4
        
        # Design pattern bonus
        design_patterns = len([p for p in self.patterns 
                             if p.pattern_type == SemanticPatternType.DESIGN_PATTERN])
        pattern_score = min(1.0, design_patterns * 0.2)
        score += pattern_score * 0.3
        total_weight += 0.3
        
        return score / total_weight if total_weight > 0 else 0.0