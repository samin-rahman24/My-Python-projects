#!/usr/bin/env python3

from poker import HandEvaluator, parse_card

def test_all_hand_types():
    """Test all poker hand types."""
    print("🧪 Testing HandEvaluator...")
    print("=" * 50)
    
    # Test cases: (cards, expected_hand_type)
    test_cases = [
        # Royal Flush
        (["AS", "KS", "QS", "JS", "TS"], "Royal Flush"),
        
        # Straight Flush
        (["9H", "8H", "7H", "6H", "5H"], "Straight Flush"),
        
        # Four of a Kind
        (["AS", "AC", "AH", "AD", "KS"], "Four of a Kind"),
        
        # Full House
        (["KS", "KC", "KH", "2S", "2C"], "Full House"),
        
        # Flush
        (["AH", "KH", "QH", "JH", "9H"], "Flush"),
        
        # Straight
        (["AS", "KC", "QH", "JD", "TS"], "Straight"),
        (["5S", "4C", "3H", "2D", "AS"], "Straight"),  # A-2-3-4-5 wheel
        
        # Three of a Kind
        (["AS", "AC", "AH", "KD", "QS"], "Three of a Kind"),
        
        # Two Pair
        (["AS", "AC", "KH", "KD", "QS"], "Two Pair"),
        
        # Pair
        (["AS", "AC", "KH", "QD", "JS"], "Pair"),
        
        # High Card
        (["AS", "KC", "QH", "JD", "9S"], "High Card"),
    ]
    
    passed = 0
    failed = 0
    
    for i, (card_strs, expected) in enumerate(test_cases, 1):
        try:
            cards = [parse_card(card_str) for card_str in card_strs]
            hand_type, rank, tie_breakers = HandEvaluator.evaluate_hand(cards)
            
            strength_percentage = HandEvaluator.get_hand_strength_percentage(hand_type)
            
            if hand_type == expected:
                print(f"✅ Test {i:2d}: {' '.join(card_strs):15} → {hand_type:15} ({strength_percentage}%)")
                passed += 1
            else:
                print(f"❌ Test {i:2d}: {' '.join(card_strs):15} → {hand_type:15} (expected: {expected})")
                failed += 1
                
        except Exception as e:
            print(f"💥 Test {i:2d}: {' '.join(card_strs):15} → ERROR: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! HandEvaluator is working correctly!")
    else:
        print("🚨 Some tests failed. Check the implementation.")

def test_best_hand_from_seven():
    """Test finding best hand from 7 cards."""
    print("\n🎯 Testing best hand selection from 7 cards...")
    print("=" * 50)
    
    # Texas Hold'em example: Player has pair of Aces
    # Board creates straight possibility
    hole_cards = ["AS", "AC"]
    community_cards = ["KH", "QD", "JS", "TS", "2C"]
    
    all_cards = [parse_card(card_str) for card_str in hole_cards + community_cards]
    
    try:
        hand_type, rank, tie_breakers, best_cards = HandEvaluator.find_best_hand(all_cards)
        
        strength_percentage = HandEvaluator.get_hand_strength_percentage(hand_type)
        
        print(f"Hole cards: {' '.join(hole_cards)}")
        print(f"Community: {' '.join(community_cards)}")
        print(f"Best hand: {hand_type}")
        print(f"Cards used: {' '.join(repr(card) for card in best_cards)}")
        print(f"Hand strength: {strength_percentage}% 📊")
        
        # Should find the straight (A-K-Q-J-T)
        if hand_type == "Straight":
            print("✅ Correctly identified the straight!")
        else:
            print(f"🤔 Found {hand_type} instead of straight")
            
    except Exception as e:
        print(f"💥 Error: {e}")

def demo_interactive_example():
    """Demo with your actual input from the game."""
    print("\n🎮 Testing your actual game example...")
    print("=" * 50)
    
    # Your example: AH KS with community 9H QS TS 4C 2D
    hole_cards = ["AH", "KS"]
    community_cards = ["9H", "QS", "TS", "4C", "2D"]
    
    all_cards = [parse_card(card_str) for card_str in hole_cards + community_cards]
    
    hand_type, rank, tie_breakers, best_cards = HandEvaluator.find_best_hand(all_cards)
    strength_percentage = HandEvaluator.get_hand_strength_percentage(hand_type)
    
    print(f"Your hole cards: {' '.join(hole_cards)}")
    print(f"Community cards: {' '.join(community_cards)}")
    print(f"Best hand: {hand_type}")
    print(f"Cards used: {' '.join(repr(card) for card in best_cards)}")
    print(f"Hand strength: {strength_percentage}% 📊")
    
    # Add strength indication
    if strength_percentage >= 50:
        print("👍 This is a decent hand!")
    else:
        print("😐 This is a weak hand")
    
    # Check if this is actually the best possible hand
    print(f"\nAnalysis: With {' '.join(hole_cards + community_cards)}")
    print(f"Best 5 cards are: {' '.join(repr(card) for card in best_cards)}")
    print(f"This makes: {hand_type} ({strength_percentage}% strength)")

if __name__ == "__main__":
    test_all_hand_types()
    test_best_hand_from_seven()
    demo_interactive_example()
