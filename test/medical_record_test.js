const MedicalRecord = artifacts.require("MedicalRecord");

contract("MedicalRecord", accounts => {
  let medicalRecord;
  const owner = accounts[0];
  const patientId = "PATIENT001";
  const reportHash = "QmTest123";
  const reportData = "Test medical record data";

  beforeEach(async () => {
    medicalRecord = await MedicalRecord.new({ from: owner });
  });

  it("should store a medical record", async () => {
    await medicalRecord.storeRecord(patientId, reportHash, reportData, { from: owner });
    
    const record = await medicalRecord.getRecord(patientId, reportHash);
    assert.equal(record.patientId, patientId, "Patient ID doesn't match");
    assert.equal(record.reportHash, reportHash, "Report hash doesn't match");
    assert.equal(record.reportData, reportData, "Report data doesn't match");
    assert.equal(record.isValid, true, "Record should be valid");
  });

  it("should update a medical record", async () => {
    await medicalRecord.storeRecord(patientId, reportHash, reportData, { from: owner });
    const newReportData = "Updated medical record data";
    
    await medicalRecord.updateRecord(patientId, reportHash, newReportData, { from: owner });
    
    const record = await medicalRecord.getRecord(patientId, reportHash);
    assert.equal(record.reportData, newReportData, "Report data wasn't updated");
  });

  it("should invalidate a medical record", async () => {
    await medicalRecord.storeRecord(patientId, reportHash, reportData, { from: owner });
    
    await medicalRecord.invalidateRecord(patientId, reportHash, { from: owner });
    
    const isValid = await medicalRecord.isRecordValid(patientId, reportHash);
    assert.equal(isValid, false, "Record should be invalid");
  });
}); 