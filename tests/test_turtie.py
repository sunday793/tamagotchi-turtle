import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.turtie import MyTurtie

class TestTurtie:
    """Unit tests for MuTurtie game logic."""

    def test_initial_state(self):
        """Test that turtie starts with correct default stats."""
        turtie = MyTurtie()
        assert turtie.health == 20
        assert turtie.satiety == 10
        assert turtie.is_healthy is True
        assert turtie.is_full is True
        assert turtie.is_sleeping is False

    def test_feed_increases_satiety(self):
        """Test that feeding increases satiety."""
        turtie = MyTurtie()
        turtie.satiety = 5
        result = turtie.feed()
        assert result is True
        assert turtie.satiety == 6
    
    def test_feed_when_full(self):
        """Test that feeding fails when turtle is full."""
        turtie = MyTurtie()
        result = turtie.feed()
        assert result is False
        assert turtie.satiety == 10
    
    def test_feed_when_sleeping(self):
        """Test that feeding fails when turtle is sleeping."""
        turtie = MyTurtie()
        turtie.satiety = 5
        turtie.is_sleeping = True
        result = turtie.feed()
        assert result is False
        assert turtie.satiety == 5
    
    def test_wash_increases_health(self):
        """Test that washing increases health."""
        turtie = MyTurtie()
        turtie.health = 10
        result = turtie.wash()
        assert result is True
        assert turtie.health == 11
    
    def test_wash_when_healthy(self):
        """Test that washing fails when health is already max."""
        turtie = MyTurtie()
        result = turtie.wash()
        assert result is False
        assert turtie.health == 20
    
    def test_decrease_satiety(self):
        """Test that satiety decreases over time."""
        turtie = MyTurtie()
        turtie.decrease_satiety()
        assert turtie.satiety == 9
        assert turtie.is_full is True
    
    def test_decrease_satiety_to_zero(self):
        """Test that satiety doesn't go below zero."""
        turtie = MyTurtie()
        turtie.satiety = 1
        turtie.decrease_satiety()
        assert turtie.satiety == 0
        assert turtie.is_full is False
    
    def test_decrease_health(self):
        """Test that health decreases over time."""
        turtie = MyTurtie()
        turtie.decrease_health()
        assert turtie.health == 19
        assert turtie.is_healthy is True
    
    def test_decrease_health_to_zero(self):
        """Test that health doesn't go below zero."""
        turtie = MyTurtie()
        turtie.health = 1
        turtie.decrease_health()
        assert turtie.health == 0
        assert turtie.is_healthy is False
