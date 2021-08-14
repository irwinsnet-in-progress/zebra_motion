
import zebra


DATA_FILE = r'C:\Users\stacy\OneDrive\Projects\zebra\zebra_data\2020wasno.jsonl'

def test_zmatch():
    zc = zebra.Competitions(DATA_FILE)
    assert zc.event_summary.path_matches.sum() == len(zc)
    qm1 = zc['2020wasno_qm1']
    assert qm1.event == '2020wasno'
    assert qm1.match == '2020wasno_qm1'
    assert qm1.blue == ['frc1318', 'frc4089', 'frc8059']
    assert qm1.red == ['frc4131', 'frc4683', 'frc2412']
    assert qm1.paths.shape[0] == 12

    assert qm1.teams['frc1318']['n'] == 1502
    assert qm1.teams['frc1318']['station'] == 'blue1'
    assert qm1.teams['frc1318']['start'] == (7.46, 16.63, 0)
    assert qm1.teams['frc1318']['end'] == (27.2, 17.69, 1502)


