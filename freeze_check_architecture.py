#!/usr/bin/env python3
"""
PHASE 1 Freeze Checklist — Quick architecture validation (no Ollama required)
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Verify all modules import correctly"""
    print("\n✓ Checking imports...")
    try:
        from ivamini.orchestrator.core import Orchestrator
        from ivamini.tasks.task import Task
        from ivamini.models.output import TaskOutput
        from ivamini.agents.analysis_agent import AnalysisAgent
        from ivamini.memory.session import SessionMemory
        from ivamini.config import load_config
        print("  ✓ All imports successful")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_task_creation():
    """Verify task creation with new signature"""
    print("\n✓ Testing task creation (fixed signature)...")
    try:
        from ivamini.orchestrator.core import Orchestrator
        
        orchestrator = Orchestrator()
        # New signature: mode, task_type, content
        task = orchestrator.create_task("QUESTION", "QUESTION", "Test?")
        
        assert task.task_id, "Task ID missing"
        assert task.mode == "QUESTION", "Mode mismatch"
        assert task.task_type == "QUESTION", "Task type mismatch"
        assert task.content == "Test?", "Content mismatch"
        
        print(f"  ✓ Task created: {task.task_id}")
        print(f"    - Mode: {task.mode}")
        print(f"    - Type: {task.task_type}")
        return True
    except Exception as e:
        print(f"  ❌ Task creation failed: {e}")
        return False

def test_memory_isolation():
    """Verify session memory is in-memory only"""
    print("\n✓ Testing session memory isolation...")
    try:
        from ivamini.memory.session import SessionMemory
        
        mem1 = SessionMemory()
        mem1.add("Entry 1")
        
        mem2 = SessionMemory()
        mem2.add("Entry 2")
        
        # Verify they're separate instances
        assert len(mem1.entries) == 1, "Memory 1 should have 1 entry"
        assert len(mem2.entries) == 1, "Memory 2 should have 1 entry"
        assert mem1.entries[0]['content'] != mem2.entries[0]['content'], "Memories should be isolated"
        
        print(f"  ✓ Session memory is isolated (in-memory only)")
        return True
    except Exception as e:
        print(f"  ❌ Memory isolation test failed: {e}")
        return False

def test_output_format():
    """Verify TaskOutput envelope structure"""
    print("\n✓ Testing TaskOutput structure...")
    try:
        from ivamini.models.output import TaskOutput
        
        sample_result = {
            "status": "SUCCESS",
            "summary": "Test summary",
            "raw_output": "Test output"
        }
        
        output = TaskOutput.from_result(
            task_id="test123",
            task_type="QUESTION",
            result=sample_result,
            duration_ms=100
        )
        
        output_dict = output.to_dict()
        
        assert output_dict['task_id'] == "test123", "Task ID mismatch"
        assert output_dict['task_type'] == "QUESTION", "Task type mismatch"
        assert output_dict['status'] == "SUCCESS", "Status mismatch"
        assert output_dict['duration_ms'] == 100, "Duration mismatch"
        assert output_dict['result'] == sample_result, "Result mismatch"
        
        print(f"  ✓ TaskOutput structure is correct")
        print(f"    Keys: {list(output_dict.keys())}")
        return True
    except Exception as e:
        print(f"  ❌ Output format test failed: {e}")
        return False

def test_error_handling():
    """Verify graceful Ollama error handling"""
    print("\n✓ Testing Ollama error handling...")
    try:
        from ivamini.llm.interface import LocalLLM
        
        llm = LocalLLM()
        
        # This will timeout or fail because Ollama isn't running
        # But the error handler should catch it
        result = llm.analyze("Test prompt")
        
        # Check that result has error handling structure
        assert 'status' in result, "Status field missing"
        assert 'duration_ms' in result, "Duration tracking missing"
        
        if result['status'] == 'ERROR':
            print(f"  ✓ Error handling works: {result.get('error', 'Error logged')[:50]}...")
        else:
            print(f"  ✓ LLM responded (Ollama is running): {result['status']}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        return False

def test_no_init_logic():
    """Verify no runtime logic in __init__.py files"""
    print("\n✓ Checking __init__.py files...")
    try:
        init_files = [
            Path(__file__).parent / "ivamini" / "__init__.py",
            Path(__file__).parent / "ivamini" / "agents" / "__init__.py",
            Path(__file__).parent / "ivamini" / "tasks" / "__init__.py",
        ]
        
        for init_file in init_files:
            if init_file.exists():
                content = init_file.read_text().strip()
                # Should be empty or comment-only
                if content and not all(line.startswith("#") or not line.strip() for line in content.split('\n')):
                    print(f"  ❌ {init_file.name} contains runtime logic")
                    return False
        
        print(f"  ✓ All __init__.py files are clean (no runtime logic)")
        return True
    except Exception as e:
        print(f"  ❌ Init file check failed: {e}")
        return False

def test_gitignore():
    """Verify .gitignore excludes runtime artifacts"""
    print("\n✓ Checking .gitignore...")
    try:
        gitignore = Path(__file__).parent / ".gitignore"
        content = gitignore.read_text()
        
        required_excludes = [
            "__pycache__",
            "venv",
            ".env",
            "*.jsonl",
            "logs/",
            "*.pyc"
        ]
        
        for exclude in required_excludes:
            if exclude not in content:
                print(f"  ⚠️  Missing .gitignore rule: {exclude}")
                return False
        
        print(f"  ✓ .gitignore has all required excludes")
        return True
    except Exception as e:
        print(f"  ❌ .gitignore check failed: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("IVAmini v1.0 FREEZE CHECKLIST — QUICK VALIDATION")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Task Creation (Fixed)", test_task_creation),
        ("Memory Isolation", test_memory_isolation),
        ("Output Format", test_output_format),
        ("Error Handling", test_error_handling),
        ("No __init__ Logic", test_no_init_logic),
        (".gitignore", test_gitignore),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"  ❌ Test exception: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed_count}/{total_count} checks passed")
    
    if passed_count == total_count:
        print("\n✅ ALL FREEZE CHECKS PASSED")
        print("System is ready for v1.0-local tag")
        sys.exit(0)
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Review failures before freezing")
        sys.exit(1)
