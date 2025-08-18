import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import swisseph as swe
from ephem.horoscope import (
    sign_from_index, 
    _get_calc_flag, 
    get_planets, 
    get_angles, 
    build_horoscope,
    SIGN_ORDER,
    PLANET_KEYS
)


class TestSignFromIndex(unittest.TestCase):
    """Test the sign_from_index function."""
    
    def test_valid_indices(self):
        """Test that valid indices (0-11) return correct signs."""
        # Test first sign (Aries = 0)
        name, data = sign_from_index(0)
        self.assertEqual(name, SIGN_ORDER[0])
        self.assertIsInstance(data, dict)
        
        # Test last sign (Pisces = 11)
        name, data = sign_from_index(11)
        self.assertEqual(name, SIGN_ORDER[11])
        self.assertIsInstance(data, dict)
        
        # Test middle sign
        name, data = sign_from_index(6)
        self.assertEqual(name, SIGN_ORDER[6])
        
    def test_invalid_indices(self):
        """Test that invalid indices raise ValueError."""
        with self.assertRaises(ValueError) as cm:
            sign_from_index(-1)
        self.assertIn("Index must be between 0 and 11", str(cm.exception))
        
        with self.assertRaises(ValueError):
            sign_from_index(12)
            
        with self.assertRaises(ValueError):
            sign_from_index(100)
    
    def test_return_format(self):
        """Test that function returns tuple of (name, data)."""
        result = sign_from_index(5)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        name, data = result
        self.assertIsInstance(name, str)
        self.assertIsInstance(data, dict)


class TestGetCalcFlag(unittest.TestCase):
    """Test the _get_calc_flag function."""
    
    def test_tropical_mode(self):
        """Test that None offset returns tropical flag."""
        result = _get_calc_flag(None)
        self.assertEqual(result, swe.FLG_SWIEPH)
    
    @patch('swisseph.set_sid_mode')
    def test_sidereal_mode_with_real_constants(self, mock_set_sid_mode):
        """Test sidereal mode using real constants."""
        from ephem.horoscope import AYANAMSAS
        
        if len(AYANAMSAS) > 1:
            # Test with a valid index
            values_list = list(AYANAMSAS.values())
            expected_value = values_list[1]  # Whatever the actual value is at index 1
            
            result = _get_calc_flag(1)
            expected_flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
            self.assertEqual(result, expected_flag)
            mock_set_sid_mode.assert_called_once_with(expected_value, 0, 0)
        else:
            self.skipTest("Need at least 2 AYANAMSAS entries for this test")
    
    def test_sidereal_mode_invalid_offset(self):
        """Test that invalid sidereal offset raises ValueError."""
        from ephem.horoscope import AYANAMSAS
        
        # Use an offset that's definitely out of range
        invalid_offset = len(AYANAMSAS) + 5
        
        with self.assertRaises(ValueError) as cm:
            _get_calc_flag(invalid_offset)
        self.assertIn("Sidereal offset index out of range", str(cm.exception))


class TestGetPlanets(unittest.TestCase):
    """Test the get_planets function."""
    
    @patch('swisseph.calc_ut')
    @patch('swisseph.split_deg')
    @patch('ephem.horoscope._get_calc_flag')
    @patch('ephem.horoscope.sign_from_index')
    def test_get_planets_basic(self, mock_sign_from_index, mock_get_calc_flag, 
                              mock_split_deg, mock_calc_ut):
        """Test basic planet calculation."""
        # Setup mocks
        mock_get_calc_flag.return_value = swe.FLG_SWIEPH
        mock_calc_ut.return_value = ([125.5], None)  # longitude
        mock_split_deg.return_value = (5, 25, 30, 0, 4)  # deg, min, sec, ?, sign_index
        mock_sign_from_index.return_value = ('Leo', {
            'trunc': 'Leo',
            'glyph': '♌',
            'trip': 'Fire',
            'quad': 'Fixed'
        })
        
        jd_now = 2460000.0
        jd_then = 2459999.0
        
        planets = get_planets(jd_now, jd_then)
        
        # Check that we got results for all planets
        self.assertEqual(len(planets), len(PLANET_KEYS))
        
        # Check structure of first planet
        planet = planets[0]
        expected_keys = ['obj_key', 'deg', 'mnt', 'sec', 'sign', 'trunc', 
                        'glyph', 'trip', 'quad', 'rx', 'lng']
        for key in expected_keys:
            self.assertIn(key, planet)
        
        # Check that calc_ut was called for each planet
        self.assertEqual(mock_calc_ut.call_count, len(PLANET_KEYS) * 2)  # now + then
    
    @patch('swisseph.calc_ut')
    @patch('swisseph.split_deg') 
    @patch('ephem.horoscope._get_calc_flag')
    @patch('ephem.horoscope.sign_from_index')
    def test_retrograde_detection(self, mock_sign_from_index, mock_get_calc_flag,
                                 mock_split_deg, mock_calc_ut):
        """Test retrograde detection logic."""
        mock_get_calc_flag.return_value = swe.FLG_SWIEPH
        mock_split_deg.return_value = (5, 25, 30, 0, 4)
        mock_sign_from_index.return_value = ('Leo', {
            'trunc': 'Leo', 'glyph': '♌', 'trip': 'Fire', 'quad': 'Fixed'
        })
        
        # Test retrograde (dd_then > dd_now)
        mock_calc_ut.side_effect = [
            ([125.5], None),  # now
            ([126.0], None),  # then (higher = retrograde)
        ] * len(PLANET_KEYS)
        
        planets = get_planets(2460000.0, 2459999.0)
        
        # All planets should be retrograde
        for planet in planets:
            self.assertTrue(planet['rx'])
    
    @patch('ephem.horoscope._get_calc_flag')
    def test_sidereal_offset_passed(self, mock_get_calc_flag):
        """Test that sidereal offset is passed to _get_calc_flag."""
        mock_get_calc_flag.return_value = swe.FLG_SWIEPH
        
        with patch('swisseph.calc_ut') as mock_calc_ut, \
             patch('swisseph.split_deg') as mock_split_deg, \
             patch('ephem.horoscope.sign_from_index') as mock_sign_from_index:
            
            # Setup mocks to prevent the unpacking error
            mock_calc_ut.return_value = ([125.5], None)
            mock_split_deg.return_value = (5, 25, 30, 0, 4)
            mock_sign_from_index.return_value = ('Leo', {
                'trunc': 'Leo', 'glyph': '♌', 'trip': 'Fire', 'quad': 'Fixed'
            })
            
            get_planets(2460000.0, 2459999.0, offset=2)
            mock_get_calc_flag.assert_called_with(2)


class TestGetAngles(unittest.TestCase):
    """Test the get_angles function."""
    
    @patch('swisseph.houses_ex')
    @patch('swisseph.split_deg')
    @patch('ephem.horoscope._get_calc_flag')
    @patch('ephem.horoscope.sign_from_index')
    def test_get_angles_basic(self, mock_sign_from_index, mock_get_calc_flag,
                             mock_split_deg, mock_houses_ex):
        """Test basic angle calculation."""
        # Setup mocks
        mock_get_calc_flag.return_value = swe.FLG_SWIEPH
        mock_houses_ex.return_value = (None, [15.5, 285.75])  # ASC, MC
        mock_split_deg.return_value = (15, 30, 0, 0, 0)  # Aries
        mock_sign_from_index.return_value = ('Aries', {
            'trunc': 'Ari',
            'glyph': '♈',
            'trip': 'Fire', 
            'quad': 'Cardinal'
        })
        
        angles = get_angles(2460000.0, 40.7, -74.0)
        
        # Should return ASC and MC
        self.assertEqual(len(angles), 2)
        
        # Check structure
        angle = angles[0]
        expected_keys = ['obj_key', 'deg', 'mnt', 'sec', 'sign', 'trunc',
                        'glyph', 'trip', 'quad']
        for key in expected_keys:
            self.assertIn(key, angle)
        
        # Check that rx is not present (angles don't go retrograde)
        self.assertNotIn('rx', angle)
        
        # Verify houses_ex was called with correct parameters
        mock_houses_ex.assert_called_once_with(2460000.0, 40.7, -74.0, b'W', swe.FLG_SWIEPH)


class TestBuildHoroscope(unittest.TestCase):
    """Test the build_horoscope function."""
    
    @patch.dict('ephem.horoscope.OBJECTS', {
        'ae': {'name': 'Sun', 'glyph': '☉'},
        'asc': {'name': 'Ascendant', 'glyph': 'Asc'}
    })
    def test_build_horoscope_structure(self):
        """Test that build_horoscope creates correct structure."""
        planets = [{
            'obj_key': 'ae',
            'deg': 15,
            'mnt': 30,
            'sec': 45,
            'sign': 'Leo',
            'trunc': 'Leo',
            'glyph': '♌',
            'trip': 'Fire',
            'quad': 'Fixed',
            'rx': True,
            'lng': 135.5125
        }]
        
        angles = [{
            'obj_key': 'asc',
            'deg': 22,
            'mnt': 15,
            'sec': 0,
            'sign': 'Gemini',
            'trunc': 'Gem',
            'glyph': '♊',
            'trip': 'Air',
            'quad': 'Mutable'
        }]
        
        horoscope = build_horoscope(planets, angles)
        
        # Check that both objects are present
        self.assertIn('ae', horoscope)
        self.assertIn('asc', horoscope)
        
        # Check Sun entry structure
        sun = horoscope['ae']
        expected_keys = ['obj_name', 'obj_glyph', 'deg', 'mnt', 'sec', 'sign',
                        'sign_trunc', 'sign_glyph', 'trip', 'quad', 'rx',
                        'full', 'short', 'glyph']
        for key in expected_keys:
            self.assertIn(key, sun)
        
        # Check specific values
        self.assertEqual(sun['obj_name'], 'Sun')
        self.assertEqual(sun['obj_glyph'], '☉')
        self.assertEqual(sun['deg'], 15)
        self.assertEqual(sun['rx'], True)
        
        # Check formatted strings
        self.assertIn('15', sun['full'])
        self.assertIn('Leo', sun['full'])
        self.assertIn(' r', sun['full'])  # retrograde indicator
        
        # Check ASC entry (no retrograde)
        asc = horoscope['asc']
        self.assertEqual(asc['rx'], False)
        self.assertNotIn(' r', asc['full'])
    
    @patch.dict('ephem.horoscope.OBJECTS', {'ae': {'name': 'Sun', 'glyph': '☉'}})
    def test_display_string_formatting(self):
        """Test the formatted display strings."""
        planets = [{
            'obj_key': 'ae',
            'deg': 5,
            'mnt': 8,
            'sec': 22,
            'sign': 'Pisces',
            'trunc': 'Pis',
            'glyph': '♓',
            'trip': 'Water',
            'quad': 'Mutable',
            'rx': False
        }]
        
        horoscope = build_horoscope(planets, [])
        
        sun = horoscope['ae']
        
        # Test full format: " 5 Pisces 8 22"
        expected_full = " 5 Pisces 8 22"
        self.assertEqual(sun['full'], expected_full)
        
        # Test short format: " 5 Pis 8"
        expected_short = " 5 Pis 8"
        self.assertEqual(sun['short'], expected_short)
        
        # Test glyph format: " 5 ♓ 8"
        expected_glyph = " 5 ♓ 8"
        self.assertEqual(sun['glyph'], expected_glyph)


class TestIntegration(unittest.TestCase):
    """Integration tests using real Swiss Ephemeris data."""
    
    @patch.dict('ephem.horoscope.OBJECTS', clear=True)
    @patch.dict('ephem.horoscope.SIGNS', clear=True) 
    @patch.dict('ephem.horoscope.AYANAMSAS', clear=True)
    def test_full_workflow_mocked(self):
        """Test complete workflow with mocked constants."""
        # Setup mock constants for ALL planet keys
        from ephem.horoscope import OBJECTS, SIGNS, PLANET_KEYS
        
        # Add objects for all planets that will be processed
        planet_objects = {}
        for i, key in enumerate(PLANET_KEYS):
            planet_objects[key] = {'name': f'Test Planet {i}', 'glyph': '☉'}
        
        planet_objects.update({
            'asc': {'name': 'Ascendant', 'glyph': 'Asc'},
            'mc': {'name': 'Midheaven', 'glyph': 'MC'}
        })
        
        OBJECTS.update(planet_objects)
        SIGNS.update({'Leo': {'trunc': 'Leo', 'glyph': '♌', 'trip': 'Fire', 'quad': 'Fixed'}})
        
        with patch('swisseph.calc_ut') as mock_calc_ut, \
             patch('swisseph.split_deg') as mock_split_deg, \
             patch('swisseph.houses_ex') as mock_houses_ex:
            
            mock_calc_ut.return_value = ([135.0], None)
            mock_split_deg.return_value = (15, 0, 0, 0, 4)  # 15° Leo
            mock_houses_ex.return_value = (None, [45.0, 225.0])
            
            # Get planets and angles
            planets = get_planets(2460000.0, 2459999.0)
            angles = get_angles(2460000.0, 40.7, -74.0)
            
            # Build horoscope
            horoscope = build_horoscope(planets, angles)
            
            # Verify we got a complete horoscope
            self.assertEqual(len(horoscope), len(PLANET_KEYS) + 2)  # planets + ASC + MC


if __name__ == '__main__':
    # Run specific test classes or all tests
    unittest.main(verbosity=2)
