"""
Database repository abstraction layer.
This allows for easy swapping of database implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime


class Repository(ABC):
    """Abstract base class for database operations"""

    @abstractmethod
    def initialize(self):
        """Initialize the database (create tables, etc.)"""
        pass

    @abstractmethod
    def create_simulation(self, input_data: Dict[str, Any]) -> int:
        """
        Create a new simulation record
        
        Args:
            input_data: Dictionary containing simulation input parameters
            
        Returns:
            The ID of the created simulation
        """
        pass

    @abstractmethod
    def get_simulation(self, simulation_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a simulation by ID
        
        Args:
            simulation_id: The ID of the simulation
            
        Returns:
            Dictionary containing simulation data or None if not found
        """
        pass

    @abstractmethod
    def update_simulation(self, simulation_id: int, results: Dict[str, Any], status: str = 'completed') -> bool:
        """
        Update a simulation with results
        
        Args:
            simulation_id: The ID of the simulation
            results: Dictionary containing calculation results
            status: Status of the simulation (default: 'completed')
            
        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_all_simulations(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all simulations with optional pagination
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of simulation dictionaries
        """
        pass

    @abstractmethod
    def delete_simulation(self, simulation_id: int) -> bool:
        """
        Delete a simulation by ID
        
        Args:
            simulation_id: The ID of the simulation
            
        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_simulation_count(self) -> int:
        """
        Get the total number of simulations
        
        Returns:
            Total count of simulations
        """
        pass

    @abstractmethod
    def get_simulations_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Get simulations within a date range
        
        Args:
            start_date: Start of the date range
            end_date: End of the date range
            
        Returns:
            List of simulation dictionaries
        """
        pass

    @abstractmethod
    def clear_all_simulations(self) -> bool:
        """
        Delete all simulations (use with caution)
        
        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dictionary containing database statistics
        """
        pass

    @abstractmethod
    def close(self):
        """Close database connection"""
        pass
