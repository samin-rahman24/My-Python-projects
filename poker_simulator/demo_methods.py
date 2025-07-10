#!/usr/bin/env python3

from poker import ExactProbabilityCalculator, parse_card

def demo_mathematical_methods():
    """Demonstrate the difference between exact and Monte Carlo methods."""
    
    print("🧮 MATHEMATICAL METHODS COMPARISON")
    print("=" * 50)
    
    # Simple heads-up scenario with pocket aces
    player_cards = [parse_card("AS"), parse_card("AC")]
    community_cards = [parse_card("KH"), parse_card("QD"), parse_card("JS")]
    
    print(f"📋 Scenario: Pocket Aces vs 1 opponent")
    print(f"🂠 Your cards: {' '.join(repr(card) for card in player_cards)}")
    print(f"🂡 Community: {' '.join(repr(card) for card in community_cards)}")
    print()
    
    # Method 1: Exact Combinatorial Analysis
    print("🧮 METHOD 1: EXACT COMBINATORIAL ANALYSIS")
    print("-" * 40)
    try:
        exact_result = ExactProbabilityCalculator.calculate_exact_probability(
            player_cards, community_cards, 1
        )
        if exact_result:
            print(f"✅ EXACT RESULT:")
            print(f"   Win: {exact_result['win_probability']:.3f}%")
            print(f"   Tie: {exact_result['tie_probability']:.3f}%")
            print(f"   Lose: {exact_result['lose_probability']:.3f}%")
            print(f"   Based on: {exact_result['total_scenarios']:,} scenarios")
            print(f"   ⭐ Mathematically perfect - no approximation!")
    except Exception as e:
        print(f"❌ Exact method failed: {e}")
    
    print()
    
    # Method 2: Monte Carlo Simulation (multiple runs to show variance)
    print("🎲 METHOD 2: MONTE CARLO SIMULATION")
    print("-" * 40)
    
    iterations_list = [1000, 10000, 100000]
    
    for iterations in iterations_list:
        mc_result = ExactProbabilityCalculator.monte_carlo_simulation(
            player_cards, community_cards, 1, iterations
        )
        print(f"📊 {iterations:,} simulations:")
        print(f"   Win: {mc_result['win_probability']:.3f}%")
        print(f"   Tie: {mc_result['tie_probability']:.3f}%")
        print(f"   Lose: {mc_result['lose_probability']:.3f}%")
        
        if exact_result:
            win_error = abs(mc_result['win_probability'] - exact_result['win_probability'])
            print(f"   Error: ±{win_error:.3f}% from exact value")
        print()

def explain_mathematical_superiority():
    """Explain why exact calculation is superior."""
    
    print("\n🎯 WHY EXACT CALCULATION IS SUPERIOR:")
    print("=" * 50)
    
    print("1. 🎯 PERFECT ACCURACY")
    print("   • Exact: 100.000% accurate")
    print("   • Monte Carlo: ~99% accurate (with enough samples)")
    print()
    
    print("2. ⚡ DETERMINISTIC RESULTS")
    print("   • Exact: Same result every time")
    print("   • Monte Carlo: Different results each run")
    print()
    
    print("3. 🧮 MATHEMATICAL RIGOR")
    print("   • Exact: Pure combinatorial mathematics")
    print("   • Monte Carlo: Statistical approximation")
    print()
    
    print("4. 📊 COMPUTATIONAL EFFICIENCY (for small scenarios)")
    print("   • Exact: Counts all possibilities once")
    print("   • Monte Carlo: Samples repeatedly")
    print()
    
    print("5. ✅ PROVABLE CORRECTNESS")
    print("   • Exact: Mathematically provable")
    print("   • Monte Carlo: Probabilistically correct")

def when_to_use_each_method():
    """Explain when to use each method."""
    
    print("\n🤔 WHEN TO USE EACH METHOD:")
    print("=" * 50)
    
    print("🧮 USE EXACT CALCULATION WHEN:")
    print("   • ≤2 opponents")
    print("   • ≤10 unknown cards total")
    print("   • <1M possible scenarios")
    print("   • Need perfect accuracy")
    print("   • Results will be used for research/theory")
    print()
    
    print("🎲 USE MONTE CARLO WHEN:")
    print("   • >2 opponents")
    print("   • >10 unknown cards")
    print("   • >1M possible scenarios")
    print("   • Speed is more important than perfect accuracy")
    print("   • ~1% error margin is acceptable")
    print()
    
    print("🚀 OUR HYBRID APPROACH:")
    print("   • Automatically chooses the best method")
    print("   • Exact when possible, Monte Carlo when necessary")
    print("   • Gives you mathematical precision OR speed")

if __name__ == "__main__":
    demo_mathematical_methods()
    explain_mathematical_superiority()
    when_to_use_each_method()
    
    print("\n🎉 CONCLUSION:")
    print("Our poker simulator uses the most mathematically rigorous")
    print("approach available, giving you perfect accuracy when possible!")
