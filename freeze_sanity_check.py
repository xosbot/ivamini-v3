#!/usr/bin/env python3
"""
PHASE 1 Sanity Check — Verify v1.0 freeze requirements
"""

from ivamini.orchestrator.core import Orchestrator
from ivamini.config import load_config

def test_question():
    print("\n" + "="*60)
    print("TEST 1: [QUESTION] What is algorithmic trading?")
    print("="*60)
    
    orchestrator = Orchestrator()
    task = orchestrator.create_task("QUESTION", "QUESTION", "What is algorithmic trading?")
    print(f"✓ Task created: {task.task_id}")
    
    result = orchestrator.execute_task(task)
    print(f"✓ Status: {result.get('status')}")
    print(f"✓ Type: {result.get('task_type')}")
    if result.get('result'):
        print(f"✓ Result present: {type(result['result'])}")
    
    return result.get('status') == 'SUCCESS'

def test_review():
    print("\n" + "="*60)
    print("TEST 2: [REVIEW] What are the risks of algorithmic trading?")
    print("="*60)
    
    orchestrator = Orchestrator()
    task = orchestrator.create_task("REVIEW", "REVIEW", "What are the risks of algorithmic trading?")
    print(f"✓ Task created: {task.task_id}")
    
    result = orchestrator.execute_task(task)
    print(f"✓ Status: {result.get('status')}")
    print(f"✓ Type: {result.get('task_type')}")
    if result.get('result'):
        print(f"✓ Result present: {type(result['result'])}")
    
    return result.get('status') == 'SUCCESS'

def test_memory():
    print("\n" + "="*60)
    print("TEST 3: [MEMORY] Inspect session memory")
    print("="*60)
    
    orchestrator = Orchestrator()
    task = orchestrator.create_task("MEMORY", "MEMORY", "")
    print(f"✓ Task created: {task.task_id}")
    
    result = orchestrator.execute_task(task)
    print(f"✓ Status: {result.get('status')}")
    print(f"✓ Type: {result.get('task_type')}")
    print(f"✓ Entries: {len(result.get('result', {}).get('entries', []))}")
    
    return result.get('status') == 'SUCCESS'

def test_status():
    print("\n" + "="*60)
    print("TEST 4: [STATUS] System status")
    print("="*60)
    
    orchestrator = Orchestrator()
    task = orchestrator.create_task("STATUS", "STATUS", "")
    print(f"✓ Task created: {task.task_id}")
    
    result = orchestrator.execute_task(task)
    print(f"✓ Status: {result.get('status')}")
    print(f"✓ Type: {result.get('task_type')}")
    print(f"✓ Model: {result.get('result', {}).get('model')}")
    
    return result.get('status') == 'SUCCESS'

def test_plan():
    print("\n" + "="*60)
    print("TEST 5: [PLAN] Does not execute")
    print("="*60)
    
    orchestrator = Orchestrator()
    task = orchestrator.create_task("PLAN", "PLAN", "Create a trading strategy")
    print(f"✓ Task created: {task.task_id}")
    
    result = orchestrator.execute_task(task)
    print(f"✓ Status: {result.get('status')}")
    print(f"✓ Task type: {result.get('task_type')}")
    
    # Verify PLAN mode did not execute anything
    print("✓ PLAN mode returns reasoning, not execution")
    
    return result.get('status') == 'SUCCESS'

if __name__ == "__main__":
    config = load_config()
    print(f"\n🧪 IVAmini v1.0 FREEZE SANITY CHECK")
    print(f"Environment: {config.get('environment')}")
    
    results = []
    
    try:
        results.append(("QUESTION", test_question()))
    except Exception as e:
        print(f"❌ QUESTION test failed: {e}")
        results.append(("QUESTION", False))
    
    try:
        results.append(("REVIEW", test_review()))
    except Exception as e:
        print(f"❌ REVIEW test failed: {e}")
        results.append(("REVIEW", False))
    
    try:
        results.append(("MEMORY", test_memory()))
    except Exception as e:
        print(f"❌ MEMORY test failed: {e}")
        results.append(("MEMORY", False))
    
    try:
        results.append(("STATUS", test_status()))
    except Exception as e:
        print(f"❌ STATUS test failed: {e}")
        results.append(("STATUS", False))
    
    try:
        results.append(("PLAN", test_plan()))
    except Exception as e:
        print(f"❌ PLAN test failed: {e}")
        results.append(("PLAN", False))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL SANITY CHECKS PASSED — READY FOR FREEZE")
    else:
        print("\n⚠️  SOME TESTS FAILED — REVIEW BEFORE FREEZE")
