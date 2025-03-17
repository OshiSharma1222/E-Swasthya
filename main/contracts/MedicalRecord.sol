// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalRecord {
    struct Record {
        string patientId;
        string reportHash;
        string reportData;
        uint256 timestamp;
        bool isValid;
    }
    
    mapping(string => mapping(string => Record)) private records;
    address private owner;
    
    event RecordStored(string patientId, string reportHash, uint256 timestamp);
    event RecordUpdated(string patientId, string reportHash, uint256 timestamp);
    event RecordInvalidated(string patientId, string reportHash);
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }
    
    function storeRecord(
        string memory _patientId,
        string memory _reportHash,
        string memory _reportData
    ) public onlyOwner {
        require(bytes(_patientId).length > 0, "Patient ID cannot be empty");
        require(bytes(_reportHash).length > 0, "Report hash cannot be empty");
        
        records[_patientId][_reportHash] = Record({
            patientId: _patientId,
            reportHash: _reportHash,
            reportData: _reportData,
            timestamp: block.timestamp,
            isValid: true
        });
        
        emit RecordStored(_patientId, _reportHash, block.timestamp);
    }
    
    function updateRecord(
        string memory _patientId,
        string memory _reportHash,
        string memory _newReportData
    ) public onlyOwner {
        require(records[_patientId][_reportHash].isValid, "Record does not exist or is invalid");
        
        records[_patientId][_reportHash].reportData = _newReportData;
        records[_patientId][_reportHash].timestamp = block.timestamp;
        
        emit RecordUpdated(_patientId, _reportHash, block.timestamp);
    }
    
    function invalidateRecord(
        string memory _patientId,
        string memory _reportHash
    ) public onlyOwner {
        require(records[_patientId][_reportHash].isValid, "Record does not exist or is already invalid");
        
        records[_patientId][_reportHash].isValid = false;
        
        emit RecordInvalidated(_patientId, _reportHash);
    }
    
    function getRecord(
        string memory _patientId,
        string memory _reportHash
    ) public view returns (
        string memory patientId,
        string memory reportHash,
        string memory reportData,
        uint256 timestamp,
        bool isValid
    ) {
        Record memory record = records[_patientId][_reportHash];
        return (
            record.patientId,
            record.reportHash,
            record.reportData,
            record.timestamp,
            record.isValid
        );
    }
    
    function isRecordValid(
        string memory _patientId,
        string memory _reportHash
    ) public view returns (bool) {
        return records[_patientId][_reportHash].isValid;
    }
} 