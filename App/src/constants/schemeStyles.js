import { StyleSheet } from 'react-native';

export const schemeCardStyles = StyleSheet.create({
  card: {
    width: 280,
    backgroundColor: '#FFFDF0', // Slight gold/yellow tint
    borderRadius: 12,
    marginRight: 12,
    marginVertical: 4,
    elevation: 3,
    shadowColor: '#B8860B', // Golden shadow
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#E6D3A3',
  },
  header: {
    padding: 12,
    backgroundColor: '#FFF8E1',
    borderBottomWidth: 1,
    borderBottomColor: '#E6D3A3',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#8B6508',
    flex: 1,
    marginRight: 8,
  },
  badge: {
    backgroundColor: '#FFD700',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  badgeText: {
    color: '#8B6508',
    fontSize: 10,
    fontWeight: 'bold',
  },
  content: {
    padding: 12,
  },
  department: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
    marginBottom: 6,
  },
  description: {
    fontSize: 13,
    color: '#333',
    marginBottom: 8,
    lineHeight: 18,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: 'bold',
    color: '#555',
    marginTop: 8,
    marginBottom: 2,
  },
  sectionText: {
    fontSize: 12,
    color: '#444',
    lineHeight: 16,
  },
});
