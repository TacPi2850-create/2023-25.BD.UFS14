def coso():    
    return'''due righe
          seconda riga'''
            
def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  # This line is optional.
    snapshot.assert_match(coso(), 'coso_output.txt')